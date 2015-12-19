# kirotuso

Twitch chat bot written in Python

# Installation
- Install Python 3.5.1
- Clone the Git repo
- Rename config.sample.ini in config.ini and edit it
- Rename commands.sample.ini in commands.ini and edit it
- Execute main.py

# How to configure
## config.ini
config.ini handles IRC and general bot settings  
_Sample config.ini_  
``` ini
[auth]
host = irc.twitch.tv
port = 6667
username = YOUR_TWITCH_BOT_USERNAME
password = YOUR_TWITCH_BOT_OAUTH_TOKEN
channel = YOUR_TWITCH_CHANNEL
timeout = 2

[chat]
startmessage = Hi! I'm Kirotuso, a Twitch chat bot! Type '!ping' to test me :)
botadmins = admin1,admin2

[debug]
showserveroutput = 0
showdebugmessages = 0
```

If you are going to run the bot on Twitch, you don't have to change `host` and `port`. `username` is your bot's Twitch username, and `password` is your bot's oauth token. You can get an oauth token [here](https://twitchapps.com/tmi). `channel` is the channel where you want to activate the bot. `timeout` is the maximum socket timeout in seconds, keep it to its default value. `startmessage` is the message sent when the bot is started. If you don't want it, set it to nothing, but **don't delete the key**. `botadmins` contains the usernames of bot admins, separated by commas. Bot admins can run special commands (type 2) , we'll se that in a moment. The `debug` section contains some debug settings. If `showserveroutput` is 1, the bot will print all the packets received from the server. If `showdebugmessages` is 1, the bot will print some debug messages.

## commands.ini
commands.ini contains all the commands.  
_Sample commands.ini_
``` ini
[cmdPing]
type = 1
trigger = !ping
response = Pong!
```
If you set your commands.ini as above, your bot will have only one command: it write "Pong!" when someone says "!ping". It's not that exciting, right? Well, you can actually do more than a simple ping/pong command. Let's have a look at all the available options.  
Every section (eg: `[cmdPing]`) represents a command. The name inside the square brackets is the command's identifier, you can set it to whatever you want. Every identifier **must be unique**, so you can't have two or more identifiers with the same name. The `type` key is the most important one, set it according to what you want to do with that command.

| **Value** | **Description** |
|-----------|-----------------|
| type=1 | Simple command |
| type=2 | Periodic command (automatically sent every _x_ messages) |
| type=3 | API command (output to chat the content of a URL) |
| type=4 | File Hook (see below) |
| type=5 | File command (output to chat the content of a file) |


### Simple command
Simple commands have `type=1`. They only need `type`,`trigger` and `response` keys to work.

| **Value** | **Description** |
|-----------|-----------------|
| type | 1 |
| trigger | The word that activates the command _(case insensitive)_ |
| response | Bot's response |
| _adminOnly_ | If 1, only admins will be able to trigger that command. _Optional_ |
| _reply_ | If 1, the user who triggered the command will be notified.  _Optional_ |

### Periodic command
Periodic commands have `type=2` and are sent automatically every _x_ messages.

| **Value** | **Description** |
|-----------|-----------------|
| type | 2 |
| period | The amount of messages before sending the response |
| response | Message to send |


### API command
API commands have `type=3`. When they are triggered, the bot reads a text from a URL and replies with that text. They work just as  Simple commands.

| **Value** | **Description** |
|-----------|-----------------|
| type | 3 |
| trigger | The word that activates the command _(case insensitive)_ |
| response | URL |
| _adminOnly_ | If 1, only admins will be able to trigger that command. _Optional_ |
| _reply_ | If 1, the user who triggered the command will be notified.  _Optional_ |


### File Hooks
File Hooks have `type=4`. When the content of a specific file changes, the bot will automatically output to chat the content of that file.

| **Value** | **Description** |
|-----------|-----------------|
| type | 4 |
| response | File path |


### File commands
File commands have `type=5` and will reply with the content of a specific file.

| **Value** | **Description** |
|-----------|-----------------|
| type | 5 |
| trigger | The word that activates the command _(case insensitive)_ |
| response | File path |
| defaultResponse | Message to send if the file is empty |
| _adminOnly_ | If 1, only admins will be able to trigger that command. _Optional_ |
| _reply_ | If 1, the user who triggered the command will be notified.  _Optional_ |


# Examples
This is an example `commands.ini`
``` ini
; !specs command
[cmdSpecs]
type=1
trigger=!specs
response=My PC specs: http://hastebin.com/rixagehefu.1c

; !website command
[cmdSpecs]
type=1
trigger=!specs
response=Check my website: http://nyodev.xyz/

; follow reminder every 20 messages
[cmdFollow]
type=2
period=20
response=Don't forget to follow me if you are enjoying the stream! :)

; Output osu's now playing song automatically
[cmdFilehook]
type=4
response=C:\OsuNpDetector\np.txt

; !np command, outputs osu's now playing song
[cmdFile]
type=5
trigger=!np
response=C:\OsuNpDetector\np.txt
defaultResponse=Nothing playing!
```

# License
This project is under the MIT License. See the LICENSE file for the full license text.
