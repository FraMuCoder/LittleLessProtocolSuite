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
from strictyaml import load, Map, Str, Int, Seq, YAMLError, Optional, Any, Enum, Seq, UniqueSeq
from jinja2 import Environment, FileSystemLoader


schema = Map({"shortName": Str(),
              "longName":  Str(),
              "minVersion":  Int(),
              "maxVersion":  Int(),
              "description": Str(),
              Optional("participants"): Seq(Map({
                  "name": Str(),
                  Optional("description"): Str()
              })),
              Optional("commands"): Seq(Map({
                  "id": Int(),
                  "shortName": Str(),
                  "longName": Str(),
                  "supportedTypes": UniqueSeq(Enum(['>', '<', '!', '#'])),
                  Optional("sinceVersion"): Int(),
                  Optional("tillVersion"): Int(),
                  "description": Str(),
                  "structureType":  Enum(['md', 'markdown', 'text']),
                  "structure": Str()
              }))
         })

def md_filter(value, deep=1):
	head = '#' * deep
	lines = str(value).splitlines(True)
	lines = [head + line if line.startswith('#') else line for line in lines]
	return "".join(lines)

def cmd_title(cmd):
  return "{} - {} ({})".format(cmd['shortName'].text, cmd['longName'].text, cmd['id'].text)

def cmd_link(cmd):
  cmd_str = "".join([a.lower() if (a.isalnum()) else '-' if a==' ' else '' for a in cmd_title(cmd)])
  return "#{}".format(cmd_str)

env = Environment(loader=FileSystemLoader(os.path.dirname(__file__)),  ### TODO
				  trim_blocks=True,
				  lstrip_blocks=True)
env.filters['md'] = md_filter;
env.filters['cmd_title'] = cmd_title;
env.filters['cmd_link'] = cmd_link;

def read_yaml(input):
    yaml_str = input.read()
    return load(yaml_str, schema)

def convert_to_md(yaml):
    global env
    template = env.get_template('yaml2md.tpl')
    return template.render(yaml=yaml)


def main():
    parser = argparse.ArgumentParser(description='Little Less Protocol yaml converter')
    parser.add_argument('-t', '--type', help='output type, default is markdown (md)', nargs=1, dest='input_type', choices=['md'], default='md')
    parser.add_argument('-i', help='input file', nargs=1, dest='input', default=[sys.stdin], type=argparse.FileType('r'))
    parser.add_argument('-o', help='output file', nargs=1, dest='output', default=[sys.stdout], type=argparse.FileType('w'))
    args = parser.parse_args()

    input = args.input[0]
    output = args.output[0]

    yaml = read_yaml(input)

    if args.input_type == 'md':
        output.write(convert_to_md(yaml))

if __name__ == '__main__':
    main()
