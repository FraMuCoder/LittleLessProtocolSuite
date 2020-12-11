# Chat - Chat Example

Supported Version: 1

Serial chat protocol.


## Commands
| ID | Short | Long name |
| --:| ----- | --------- |
| [8](#log--login-8) | [LOG](#log--login-8) | [Login](#log--login-8) |
| [9](#msg--message-9) | [MSG](#msg--message-9) | [Message](#msg--message-9) |
| [10](#lst--user-list-10) | [LST](#lst--user-list-10) | [User list](#lst--user-list-10) |


- - -

### LOG - Login (8)
Login to chat system.
If the user name is not known at chat system a new account is created.


#### Data structure


- - -

Senders: Client

Receivers: Server

Message types: >

Client tries to login at server.

| Param   | Length | Description
| ------- | ------:| -----------
| userLen |      1 | Length of user name (binary, 1..10)
| user    |  1..10 | User name (ASCII)
| pwLen   |      1 | Length of password (binary, 4..20)
| pw      |  4..20 | Password (ASCII)


- - -

Senders: Server

Receivers: Client

Message types: <

Server sends login result to client.

| Param  | Length | Description
| ------ | ------:| -----------
| result |      1 | 0 => OK, 1 => error (binary)


- - -

### MSG - Message (9)
Send a chat message.

#### Data structure


- - -

Senders: Client

Receivers: Server

Message types: >

Client sends a message to server.
There is no response from server.


| Param | Length | Description
| ----- | ------:| -----------
| text  | 1..100 | Chat message (ASCII)


- - -

Senders: Server

Receivers: Client

Message types: <

Server sends a message from a client to an other client.

| Param   | Length | Description
| ------- | ------:| -----------
| userLen |      1 | Length of user name (binary, 1..10)
| user    |  1..10 | User name (ASCII)
| text    | 1..100 | Chat message (ASCII)


- - -

### LST - User list (10)
List logged in users.

A typical sequence is:

1. `>:LST:00::FF`
2. `#:LST:05:"UserA":FF`
3. `#:LST:05:"UserB":FF`
4. `#:LST:05:"UserC":FF`
5. `<:LST:02:0300:FF`


#### Data structure


- - -

Senders: Client

Receivers: Server

Message types: >

Client requests the list of logged in users.

Empty data

- - -

Senders: Server

Receivers: Client

Message types: #

Server sends one of the logged in users.
The server send one message of this type for every logged in user also the requested user.
This messages are send before result is send.


| Param | Length | Description
| ----- | ------:| -----------
| user  |  1..10 | User name (ASCII)


- - -

Senders: Server

Receivers: Client

Message types: <

Sever finish the client request to list all logged in users.

| Param  | Length | Description
| ------ | ------:| -----------
| count  |      1 | User count (0..255) (binary)
| result |      1 | 0 => OK, 1 => error (binary)

