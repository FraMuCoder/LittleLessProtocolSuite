# Little Less Protocol Suite

This repository collects documentations and tools for the Little Less Protocol.

**Please note Little Less Protocol is still under development there may be incompatible changes.**

## What is the Little Less Protocol

[Little Less Protocol](doc/LittleLessProtocol.md) is a simple serial protocol for little microcontrollers.
In comparison to other protocols Little Less Protocol uses less buffers and less states.
Also you application not need full buffers but if you want to use them,
they are owned by the application, so your application has the full control over it.

There is also a layer for basic protocol handling ([Little Less Base](doc/LittleLessBase.md))
like check if there is the right communication participant and it uses a compatible version of the protocol.
If you do not need such thinks you can omit this layer.

Because every project needs other data and commands to send you can design you individual protocol.
Therefore you can use a YAML description. This description can be used by other tools e.g. to generate
protocol documentation or even a code skeleton for your project.

The first implementation (under development but already usable):

[Little Less Protocol for Arduino (develop)](https://github.com/FraMuCoder/LittleLessProtocol/tree/develop)

More implementations will follow.
If you want to implement Little Less Protocol you should read the [Little Less Protocol specification](doc/LittleLessProtocol.md)

## Getting Started

1. [Decide if Little Less Protocol is the right for your project](#decide-if-little-less-protocol-is-the-right-for-your-project)
2. [Design you individual protocol](#design-your-individual-protocol)
3. [Generate the protocol documentation](#generate-the-protocol-documentation)
4. [Generate the code skeleton for your project](#generate-the-code-skeleton-for-your-project)
5. [Implement your project](#implement-your-project)

### Decide if Little Less Protocol is the right for your project

Little Less Protocol may fit to your project if...

- you are looking for a serial protocol for small microcontroller
- less memory consumption is more important than a quickly programmed solution
- you can process received data in chunks or even byte for byte
- you want to envelop you project step by step and need a versionable protocol
- you need to care if both communication participants fit together
- you like design generated documentation and code

Little Less Protocol may not fit to your project if...

- your system have enough memory to handle all data at once
  - Note: Little Less Protocol may still work but you may also find an easier to handle protocol
- you need a fixed API but can not wait till Little Less Protocol first released version

### Design your individual protocol

You can use the [Chat protocol](examples/Chat.yaml) as base to design your individual protocol.
Please read the [Little Less Protocol YAML schema](doc/yaml.md) for more information.

To verify you can use `yaml2x.py`. Therefore you need python3 with strictyaml and Jinja2.

On Linux just call the following commands to install all you need:
```bash
cd <PATH_TO_LITTLE_LESS_PROTOCOL_SUITE>
python3 -m venv env
source env/bin/activate
pip install strictyaml
pip install Jinja2
```

To verify just call:
```bash
./tools/yaml2x.py -i <PATH_TO_YOUR_YAML_FILE>
```

If there is no error output you yaml file is probably fine. Currently not all
possible structural defects are tested.

### Generate the protocol documentation

You can use `yaml2x.py` also to generate a markedown documentation.

On Linux just call:
```
./tools/yaml2x.py -a md -i <PATH_TO_YOUR_YAML_FILE> -o <NEW_MD_FILE>
```

Example output: [Chat protocol](examples/Chat.md)

### Generate the code skeleton for your project

Currently only code for Arduino IDE can be generated.
Again use `yaml2x.py` also to generate the code.

On Linux just call:
```
./tools/yaml2x.py -a ino -i <PATH_TO_YOUR_YAML_FILE> -o <NEW_INO_FILE>
```

### Implement your project

Of course it is up to you to implement the application logic but some tips may follow here later.

## License

Little Less Protocol Suite is distributed under the [MIT License](./LICENSE).
