# Little Less Protocol

Little Less Protocol (LLP) is a simple serial protocol for little microcontrollers.
In comparison to other protocols Little Less Protocol uses less buffers and less states.
Also you application not need full buffers but if you want to use them,
they are owned by the application, so your application has the full control over it.

There will be two versions an ASCII (A) and a binary (B) Version.

Little Less Protocol A, will of cause only uses ASCII characters but you can send binary data as well.
It will be coded as hex string.
This protocol version is ideal to work with any serial terminal or other tools, that can handle ASCII
based serial communications. Therefore it is ideal for a developing phase of a project.

Little Less Protocol B will use any possible byte not limited to ASCII. Therefore data frames are much
compacter but you can not use every tool for testing. If the other side of the communication is no
microcontrollers you may also need other implementations of this protocol maybe in different languages.

## Requirements

These requirements should allow you to reprogram Little Less Protocol.

## General requirements

### Main requirements

- LLP should use as less RAM as possible
- LLP should also use less flash memory if possible
- A full duplex communication should be possible
- A chained communication (`A <=> B <=> C`) should be possible
- The checksum for Little Less Protocol A and Little Less Protocol B shold be identically
  - Note: Just the internal value must be identically the transmitt encoding may differ

### Frame requirements

- The communication should be frame based.
- A frame should have a well known start and/or end
  - Note: Even after receiving a corrupted frame there should be a point to find back to valid frames
- A frame should have a type to determine a special protocol behavior
  - Note: A behavior could be: "for this type A a response must be send but for type B no response is needed"
- There must be at least the following types
  - request
  - response
  - error
  - update
- The meaning of the types (behavior) is defined by the application not the LLP
- A frame should have a command ID to determine the function this frame is for.
- Command ID should be defined by the application not the LLP it self
- There should be at least 255 commands ID allowed
- A frame should have a length field to determine the size of user data
- A frame should have 0 to 255 bytes of user data
- The structure of the user data is defined by the application depending on frame type and command ID
- The frame should have a checksum
- The algorithm for the checksum is not part of LLP so you can share one you have already in use
- The checksum should include frame type, command ID, length and user data
- It should be possible to deactivate checksum calculation and checks at least by setting
  an algorithm which always returns the same value

### API requirements

## Little Less Protocol A requirements

Example: `>ver:0B:11111134"Test""App":FF`

### Main requirements

- Frames should be easy to read
- Only ASCII character should be send including carriage return (\r) and newline (\n)
- It should be possible to send non LLP ASCII data as long as it is ended by a line separator (\r and/or \n)
  - Note: So you can still send debug messages

### Frame requirements

- Every Frame is ended by a carriage return (\r) and a newline (\n)
- The receiver should also accept only a carriage return (\r) or only a newline (\n)
- The first character of a frame is the frame type
- Only the following characters as frame types are allowed
  - `>` as request (internal value 0)
  - `<` as response (internal value 1)
  - `!` as error (internal value 2)
  - `#` as update (internal value 3)
- If an other character was received as first character, the current frame should be ignored till
  receiving a carriage return (\r) or a newline (\n)
- After frame type follows the command ID.
- The command ID is an exact 3 character long ASCII string
- After the command ID follows the separator 1 `:`
- After the separator 1 follows the data length
- The data length is encoded as exact 2 character long hex string
- After the data length follows the separator 2 `:`
- After the separator 2 follows the data field
  - Note: There may be an empty data field if data length is `00`
- Bytes in data filed may be encoded as exact 2 character long hex string
- Bytes in data field may be encoded as ASCII characters
- By default data field starts with hex encoding
- To switch between hex and ASCII encoding a `"` must be send
- Only ASCII characters from including 0x20 (space) till including 0x7F (DEL) are allowed in ASCII encoding
- In ASCII encoding the backspace `\` is interpreted as escape character
- The sender should escape the following character
  - `\` by sending `\\`
  - `"` by sending `\"`
- The receiver can accept more escaped character but not carriage return (0x0D) or newline (0x0A)
- After the (maybe empty) data field follows the separator 3 `:`
  - Note: If data length is `00` there are just two separators behind each other
- After the separator 3 follows the checksum
- The checksum is encoded as exact 2 character long hex string
- For checksum calculation the following bytes in the following order are used
  - Internal value of frame type (0 - 3)
  - Internal value of command ID (0 - 254) defined by application
  - Binary presentation of data length (not 2 hex characters)
  - Binary presentation of data files (not hex string and not escaping character or `"`
    as encoding switching character)
- After the checksum the frame ends as described above
- Every hex character can be send with upper or lower case characters

## Little Less Protocol B requirements

TODO