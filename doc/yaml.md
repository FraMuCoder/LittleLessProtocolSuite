# Little Less Protocol YAML schema

Please use only [strictyaml](https://hitchdev.com/strictyaml/) style.

```yaml
name:         My personal protocol  # Name of your protocol
code:         Unique name           # 1 till 15 ASCII chars
minVersion:   1                     # 0..15
maxVersion:   2                     # 0..15 minVersion <= maxVersion
description:  |
              You can use markdown to describe your individual application protocol.
baseProtocol: LittleLessBase        # optional, without 'A' or 'B' at the end
participants:                       # optional, zero or at least two participants
    - name:         PC
      description:  |               # optional
                    Again you can use markdown.
    - name:         Arduino
      description:  Also just a line is possible.
messageTypes:                       # optional
    - id:           1               # 0..7
      name:         replay          # you can rename fixed types if you want
      code:         '<'             # ids 0..3 have fixed codes ('>', '<', '!', '#')
      description:  |               # optional
                    Use markdown to describe the message type.
commands:                           # list all your commands, at least one
    - id:           8               # unique 0..254, if baseProtocol is LittleLessBase start with 8
      name:         Alphabet        # human readable name
      code:         ABC             # exact 3 ASCII chars
      sinceVersion: 1               # optional, 0..15
      tillVersion:  2               # optional, 0..15 
      description:  |               # optional
                    Use markdown to describe your command.
      messages:                     # at least one message
          - senders:                # optional, use names from participants
                - PC
            receivers:              # optional, use names from participants
                - Arduino
            messageTypes:           # list supported messages types ('>', '<', '!', '#')
                - '>'
                - '#'
            description:    |       # optional
                            Use markdown to describe the message type of this command.
            structureType:  markdown  # currently only markdown is supported
            structureDesc:  |
                            Describe the data structure using markdown.
          - senders:
                - Arduino
            receivers:
                - PC
            messageTypes:
                - '<'
            structureType:  markdown
            structureDesc:  |
                            | Param | Len  | Description
                            | ----- | ----:| -----------
                            | len   |    1 | Length of alpha (binary, 1..100)
                            | alpha |  len | Alphabet (ASCII)
```

**name**: This is the name of your protocol. It is also used as class name.
Therefore Spaces and not suitable characters are removed first.

**code**: This should be a unique name to distinguish this protocol from others.
For protocols based on LittleLessBase this is used as AppName so it should have not more than 15 characters.

**minVersion / maxVersion**: This is the version range of your protocol this documentation is for.

**description**: Describe your protocol.

**baseProtocol**: This is typical `LittleLessProtocol` or `LittleLessBase`. If left `LittleLessProtocol` is assumed.
Note there is no suffix `A` or `B`.

You can also enter an other `LittleLessProtocol` bases protocol class name to derive from this.

**participants**: Here you can list you communication sides. There should be at least two.

**messageTypes**: This is currently not used.

**commands**: List all your commands.

command / **id**: This is the internal number of a command. For `LittleLessProtocol` based protocols you should start with 0.
For `LittleLessProtocol` based protocols you should start with 8. The maximum number is 254.

Currently you must list you command with ascending ids and there must not be a gap.

command / **name**: The command name.

command / **code**: This is the 3 letter code used for the ASCII Version of `LittleLessProtocol`

**sinceVersion / tillVersion**: Here you can enter the version since when this command was add and till when it is supported.

command / **description**: You can describe your command here or later for each message.

**messages**: The command is send in a message. There could be different types of messages for the same command,
e.g. the one side send a request and the other side must answer with a response or an error.
All this message types could have different data therefore you can list all kinds of messages here.
If the data structure differs you should add a new message description.
If the data structure is identical to all types you can describe this as one message.

**senders / receivers**: List the senders and receivers of a message. This is only possible if **participants** was entered. Just list the names.

messages / **messageTypes**: List the suppotred messages types ('>', '<', '!', '#').

messages / **description**: Descripe your message.

**structureType**: This defines the format of **structureDesc**. Currently only `markedown` is supported.

**structureDesc**: Descripe the data structure of this message.
