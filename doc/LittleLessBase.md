# LittleLessBase - Little Less Base

Supported Version: 1

Basic protocol features like compatibility version check or echo service.

There is an application name and several versions.

The application name (AppName) gives you individual designed protocol a name, e.g. if you need a protocol for a chat system
the name could be "Chat" or "ChatProtocol". A the beginning the participants exchange there application name, if its differs
the communication stops. The check is case sensitive, so "Chat" and "chat" are different protocols.

Versions are coded in on byte. In this byte a range of supported versions is stored. For example 0x42 means
a supported range from version 2 till version 4. If one side has the versions 0x42 and the other side has the versions 0x31
the common versions are 0x32 because this version can be handled by all sides. The current used version is always the highest
possible version.

The following versions have to be considered:

*BaseVersions*: This are the supported versions of Little Less Protocol and Little Less Base. The application can not change this.
This versions will be increased if Little Less Protocol or Little Less Base get a new behavior on serial side.
New API features will not change this versions.

*AppVersions*: This are the supported versions of you individual designed application protocol. You have the full control over
this versions. This is not you full application or project version so you should not increase this versions just if your
application gets a new version. Change this only if the protocol get new features or different behouvior.
Please consider, there are only 16 versions. If you need more, you can change the AppName e.g. from "Chat" to "Chat2".
Of course this is always an incompatible version, you application can not support some versions from "Chat" and "Chat2".

*AgreedVersions*: This are the common versions of all other version but the BaseVersions. It will not only consider the own
versions but also the versions of the other communication participants. This must be send to other participants when ever it change,
so all sides known the set of version which can be understand from all.

*RunTimeVersions*: This version is set by the application. You can uses this to propagate *AgreedVersions* from an other communication
in a chained communication design.


## Commands
| ID | Short | Long name |
| --:| ----- | --------- |
| [0](#ver---version-0) | [ver](#ver---version-0) | [Version](#ver---version-0) |
| [1](#ech---echo-1) | [ech](#ech---echo-1) | [Echo](#ech---echo-1) |
| [2](#dbg---debug-2) | [dbg](#dbg---debug-2) | [Debug](#dbg---debug-2) |


- - -

### ver - Version (0)
Exchange supported application name and supported protocol versions.

No other commands should be send before a version was exchanged.
If application name from other side differs or an incompatible version was received no further communication should take place.
Of course new Version commands are still allowed.

A Version request ('>') must be answered with a Version result ('<').
A Version update ('#') will be send after internal version changes. Such a change may be triggered by application, e.g.
if a third participant in a chained communication has sends its versions to a middle participant.


#### Data structure


- - -



Message types: >, <, #


Example: `>ver:0B:11111143"Test""App":FF`

| Param          | Len   | Description
| -------------- | -----:|------------------------------------------------------------------------------------------
| BaseVersions   |     1 | Versions of underlying protocol (Little Less Protocol and Base), currently 0x11
| AppVersions    |     1 | Supported application versions of sender
| AgreedVersions |     1 | Currently agreed versions, this is always <= SenderVersion
| Length         |     1 | Upper nibble: length of AppName (n), Lower nibble: length of AppExtra (m)
| AppName        | 0..15 | Application protocol name (max. 15 characters)
| AppExtra       | 0..15 | Extra name (max. 15 characters)

Extra name is currently not evaluated. This may be used to name the participant.


- - -

### ech - Echo (1)
Echoservice to check if the other side is sill there.

A Echo request ('>') must be answered with a Echo result ('<').
All data from the request must be copied to the result.


#### Data structure


- - -



Message types: >, <


Example: `>ech:01:AB:FF`

There is only one data byte which must be copied to the answer.


- - -

### dbg - Debug (2)
Use this command to send debug messages.


#### Data structure


- - -



Message types: #


Example: `#dbg:0C:"Test message":FF`

This messages just contains a string. There is no terminating NULL byte.

