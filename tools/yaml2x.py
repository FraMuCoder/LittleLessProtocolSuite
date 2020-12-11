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
  'md'  : 'yaml2md.md.jinja2',
  'ino' : 'yaml2ino.cpp.jinja2'
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

def verify(yaml):
  return True

def md_filter(value, deep=1):
	head = '#' * deep
	lines = str(value).splitlines(True)
	lines = [head + line if line.startswith('#') else line for line in lines]
	return "".join(lines)

def cmd_title(cmd):
  return "{} - {} ({})".format(cmd['code'].text, cmd['name'].text, cmd['id'].text)

def cmd_link(cmd):
  cmd_str = "".join([a.lower() if (a.isalnum()) else '-' if a==' ' else '' for a in cmd_title(cmd)])
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
      print(error)
      return None

def convert(type, context):
    global env, templates_names
    templates_name = templates_names[type]
    template = env.get_template(templates_name)
    return template.render(context)


def main():
    parser = argparse.ArgumentParser(description='Little Less Protocol yaml converter')
    parser.add_argument('-a', '--action', help='action, default is verify (ver)', nargs=1, dest='action', choices=['ver', 'md', 'ino'], default=['ver'])
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
