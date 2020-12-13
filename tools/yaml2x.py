#!/usr/bin/env python3
# Little Less Protocol Suite - yaml converter
# Copyright (C) 2020 Frank Mueller
#
# SPDX-License-Identifier: MIT
#
# This tool converts a Little Less Protocol yaml file to an other format.
# The following output formatas are supported:
#  - markdown file
#
# To run this tool you will need python3 with strictyaml and Jinja2.
#

import argparse
import sys
import os
import re
from strictyaml import load, Map, Str, Int, Seq, YAMLError, Optional, Any, Enum, Seq, UniqueSeq
from jinja2 import Environment, FileSystemLoader

templates_names = {
  'md'        : 'yaml2md.md.jinja2',
  'ino'       : 'yaml2ino.cpp.jinja2',
  'ino-main'  : 'yaml2ino-main.cpp.jinja2',
  'ino-extra' : 'yaml2generic_class_implementation.cpp.jinja2'
}

schema = Map({"name": Str(),
              "code":  Str(),
              "minVersion":  Int(),
              "maxVersion":  Int(),
              "description": Str(),
              Optional("baseProtocol") : Str(),
              Optional("participants"): Seq(Map({
                  "name": Str(),
                  Optional("description"): Str()
              })),
              Optional("messageTypes"): Seq(Map({
                  "id": Int(),
                  "name": Str(),
                  "code" : Str(),
                  Optional("description"): Str()
              })),
              "commands": Seq(Map({
                  "id": Int(),
                  "name": Str(),
                  "code": Str(),
                  Optional("sinceVersion"): Int(),
                  Optional("tillVersion"): Int(),
                  Optional("description"): Str(),
                  "messages": Seq(Map({
                    Optional("senders") : Seq(Str()),
                    Optional("receivers") : Seq(Str()),
                    "messageTypes": UniqueSeq(Enum(['>', '<', '!', '#'])),
                    Optional("description"): Str(),
                    "structureType":  Enum(['md', 'markdown', 'text']),
                    "structureDesc": Str()
                  }))
              }))
         })

def output_yaml_lines(yaml):
  indent = "  "
  print(indent + "line: " + str(yaml.start_line), file=sys.stderr)
  for line in yaml.lines().splitlines():
    print(indent*2 + line, file=sys.stderr)

def verify(yaml):
  not_ascci_range = re.compile('[^ -~]').search

  if (len(yaml['code'].value) < 1) or (len(yaml['code'].value) > 15):
    print("Warning: Protocol 'code' should have a length of 1 and 15 characters but there are {}. Code generation may fail.".format(
        len(yaml['code'].value)), file=sys.stderr)
    output_yaml_lines(yaml['code'])

  if not_ascci_range(yaml['code'].value):
    print("Warning: Protocol 'code' should have only ASCII characters in range from 0x20 (space) till 0x7E (~). Code generation may fail.",
        file=sys.stderr)
    output_yaml_lines(yaml['code'])

  
  if (yaml['minVersion'].value < 0) or (yaml['minVersion'].value > 15):
    print("Error: 'minVersion' must be in range of 0 and 15 but is {}.".format(yaml['minVersion'].value), file=sys.stderr)
    output_yaml_lines(yaml['minVersion'])
    return False

  if (yaml['maxVersion'].value < 0) or (yaml['maxVersion'].value > 15):
    print("Error: 'maxVersion' must be in range of 0 and 15 but is {}.".format(yaml['maxVersion'].value), file=sys.stderr)
    output_yaml_lines(yaml['maxVersion'])
    return False

  if yaml['minVersion'].value > yaml['maxVersion'].value:
    print("Error: 'minVersion' must be less or equal to 'maxVersion' but {} > {}.".format(
        yaml['minVersion'].value, yaml['maxVersion'].value), file=sys.stderr)
    output_yaml_lines(yaml['minVersion'])
    output_yaml_lines(yaml['maxVersion'])
    return False

  participants = []
  if 'participants' in yaml:
    for participant in yaml['participants']:
      participants.append(participant['name'].value)
    if len(participants) < 2:
      print("Warning: If 'participants' are mentioned there should be at least two but are {}.".format(len(participants)),
        file=sys.stderr)
      output_yaml_lines(yaml['participants'])

  ids = []
  id_line = []
  last_id = None

  for cmd in yaml['commands']:
    if (cmd['id'].value < 0) or (cmd['id'].value > 254):
      print("Error: 'id' must be in range of 0 and 254 but is {}.".format(cmd['id'].value), file=sys.stderr)
      output_yaml_lines(cmd['id'])
      return False

    if cmd['id'].value in ids:
      print("Error: 'id' must be unique but 'id' {} first found in line {}.".format(
          cmd['id'].value, id_line[ids.index(cmd['id'].value)]), file=sys.stderr)
      output_yaml_lines(cmd['id'])
      return False
    
    ids.append(cmd['id'].value)
    id_line.append(cmd['id'].start_line)

    if last_id != None:
      if cmd['id'].value != (last_id + 1):
        print("Warning: 'id's should be sequential without a gap but after {} follows {}. Code generation may fail.".format(
            last_id, cmd['id'].value), file=sys.stderr)
        output_yaml_lines(cmd['id'])
    
    last_id = cmd['id'].value

    if (len(cmd['code'].value) != 3):
      print("Warning: Command 'code' should have a length of 3 but has {}. Code generation may fail.".format(
          len(cmd['code'].value)), file=sys.stderr)
      output_yaml_lines(cmd['code'])

    if not_ascci_range(cmd['code'].value):
      print("Warning: Command 'code' should have only ASCII characters in range from 0x20 (space) till 0x7E (~). Code generation may fail.",
          file=sys.stderr)
      output_yaml_lines(cmd['code'])

    if 'sinceVersion' in cmd:
      if (cmd['sinceVersion'].value < 0) or (cmd['sinceVersion'].value > 15):
        print("Error: 'sinceVersion' must be in range of 0 and 15 but is {}.".format(cmd['sinceVersion'].value), file=sys.stderr)
        output_yaml_lines(cmd['sinceVersion'])
        return False
      
      if (cmd['sinceVersion'].value < yaml['minVersion'].value) or (cmd['sinceVersion'].value > yaml['maxVersion'].value):
        print("Error: 'sinceVersion' must be in range of 'minVersion' ({}) and 'maxVersion' ({}) but is {}.".format(
            yaml['minVersion'].value, yaml['maxVersion'].value, cmd['sinceVersion'].value), file=sys.stderr)
        output_yaml_lines(cmd['sinceVersion'])
        return False

    if 'tillVersion' in cmd:
      if (cmd['tillVersion'].value < 0) or (cmd['tillVersion'].value > 15):
        print("Error: 'tillVersion' must be in range of 0 and 15 but is {}.".format(cmd['tillVersion'].value), file=sys.stderr)
        output_yaml_lines(cmd['tillVersion'])
        return False

      if (cmd['tillVersion'].value < yaml['minVersion'].value) or (cmd['tillVersion'].value > yaml['maxVersion'].value):
        print("Error: 'tillVersion' must be in range of 'minVersion' ({}) and 'maxVersion' ({}) but is {}.".format(
            yaml['minVersion'].value, yaml['maxVersion'].value, cmd['tillVersion'].value), file=sys.stderr)
        output_yaml_lines(cmd['tillVersion'])
        return False

    if ('sinceVersion' in cmd) and ('tillVersion' in cmd):
      if cmd['sinceVersion'].value > cmd['tillVersion'].value:
        print("Error: 'sinceVersion' must be less or equal to 'tillVersion' but {} > {}.".format(
            cmd['sinceVersion'].value, cmd['tillVersion'].value), file=sys.stderr)
        output_yaml_lines(cmd['sinceVersion'])
        output_yaml_lines(cmd['tillVersion'])
        return False
    
    for msg in cmd['messages']:
      if 'senders' in msg:
        for sender in msg['senders']:
          if sender.value not in participants:
            print("Warning: Sender should be in 'participants' list but is not. Use some of this: {}".format(
                ", ".join(participants)), file=sys.stderr)
            output_yaml_lines(sender)

      if 'receivers' in msg:
        for receiver in msg['receivers']:
          if receiver.value not in participants:
            print("Warning: Receiver should be in 'participants' list but is not. Use some of this: {}".format(
                ", ".join(participants)), file=sys.stderr)
            output_yaml_lines(receiver)

  return True

def md_filter(value, deep=1):
	head = '#' * deep
	lines = str(value).splitlines(True)
	lines = [head + line if line.startswith('#') else line for line in lines]
	return "".join(lines)

def cmd_title(cmd):
  return "{} - {} ({})".format(cmd['code'].text, cmd['name'].text, cmd['id'].text)

def cmd_link(cmd):
  cmd_str = "".join([a.lower() if (a.isalnum()) else '-' if a in ' -' else '' for a in cmd_title(cmd)])
  return "#{}".format(cmd_str)

def identifier(s, firstLow=False):
  strs = re.sub("[^a-zA-Z0-9]", " ", str(s)).split()
  strs = [s.capitalize() for s in strs]
  if firstLow:
    strs[0] = strs[0][0].lower() + strs[0][1:]
  ident = "".join(strs)
  if ident[0].isdigit():
    return "_" + ident
  else:
    return  ident

def upper_identifier(s):
  return re.sub("[^a-zA-Z0-9]", "_", str(s)).upper()

def comment(s, commentStr="// "):
  return (commentStr + commentStr.join(s.splitlines(keepends=True))).strip('\n\r')

env = Environment(loader=FileSystemLoader(os.path.dirname(__file__)),
				  trim_blocks=True,
				  lstrip_blocks=True)
env.filters['md'] = md_filter
env.filters['cmd_title'] = cmd_title
env.filters['cmd_link'] = cmd_link
env.filters['identifier'] = identifier
env.filters['upper_identifier'] = upper_identifier
env.filters['comment'] = comment

def read_yaml(input):
    yaml_str = input.read()

    try:
      return load(yaml_str, schema)
    except YAMLError as error:
      print("Error: {}".format(error), file=sys.stderr)
      return None

def convert(type, context):
    global env, templates_names
    templates_name = templates_names[type]
    template = env.get_template(templates_name)
    return template.render(context)


def main():
    parser = argparse.ArgumentParser(description='Little Less Protocol yaml converter')
    parser.add_argument('-a', '--action', help='action, default is verify (ver)', nargs=1, dest='action', 
                        choices=['ver', 'md', 'ino', 'ino-main', 'ino-extra'], default=['ver'])
    parser.add_argument('-s', '--suffix', help='Protocol suffix, default "A"', nargs='?', dest='suffix', const='', default='A')
    parser.add_argument('-p', '--participant', help='Protocol participant', nargs=1, dest='participant', default=[''])
    parser.add_argument('-i', help='input file', nargs=1, dest='input', default=[sys.stdin], type=argparse.FileType('r'))
    parser.add_argument('-o', help='output file', nargs=1, dest='output', default=[sys.stdout], type=argparse.FileType('w'))
    args = parser.parse_args()

    input = args.input[0]
    output = args.output[0]
    action = args.action[0]
    suffix = args.suffix
    participant = args.participant[0]

    yaml = read_yaml(input)

    if yaml == None:
      sys.exit(1)

    if not verify(yaml):
      sys.exit(1)

    if action != 'ver':
      context = {
        'yaml'        : yaml,
        'suffix'      : suffix,
        'participant' : participant
      }
      output.write(convert(action, context))

if __name__ == '__main__':
    main()
