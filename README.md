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
<table>
<thead>
    <tr><td>**Value**</td><td>**Description**</td</tr>
</thead>
<tbody>
    <tr><td>type=1</td><td>Simple command</td></tr>
    <tr><td>type=2</td><td>Periodic command (automatically sent every _x_ messages)</td></tr>
    <tr><td>type=3</td><td>API command (output to chat the content of a URL)</td></tr>
    <tr><td>type=4</td><td>File Hook (see below)</td></tr>
    <tr><td>type=5</td><td>File command (output to chat the content of a file)</td></tr>
</tbody>
</table>


### Simple command
Simple commands have `type=1`. They only need `type`,`trigger` and `response` keys to work.
<table>
<thead>
    <tr><td>**Value**</td><td>**Description**</td</tr>
</thead>
<tbody>
    <tr><td>type</td><td>1</td></tr>
    <tr><td>trigger</td><td>The word that activates the command _(case insensitive)_</td></tr>
    <tr><td>response</td><td>Bot's response</td></tr>
    <tr><td>_adminOnly_</td><td>If 1, only admins will be able to trigger that command. _Optional_</td></tr>
    <tr><td>_reply_</td><td>If 1, the user who triggered the command will be notified.  _Optional_</td></tr>
</tbody>
</table>


### Periodic command
Periodic commands have `type=2` and are sent automatically every _x_ messages.
<table>
<thead>
    <tr><td>**Value**</td><td>**Description**</td</tr>
</thead>
<tbody>
    <tr><td>type</td><td>2</td></tr>
    <tr><td>period</td><td>The amount of messages before sending the response</td></tr>
    <tr><td>response</td><td>Message to send</td></tr>
</tbody>
</table>


### API command
API commands have `type=3`. When they are triggered, the bot reads a text from a URL and replies with that text. They work just as  Simple commands
<table>
<thead>
    <tr><td>**Value**</td><td>**Description**</td</tr>
</thead>
<tbody>
    <tr><td>type</td><td>3</td></tr>
    <tr><td>trigger</td><td>The word that activates the command _(case insensitive)_</td></tr>
    <tr><td>response</td><td>URL</td></tr>
    <tr><td>_adminOnly_</td><td>If 1, only admins will be able to trigger that command. _Optional_</td></tr>
    <tr><td>_reply_</td><td>If 1, the user who triggered the command will be notified.  _Optional_</td></tr>
</tbody>
</table>


### File Hooks
File Hooks have `type=4`. When the content of a specific file changes, the bot will automatically output to chat the content of that file.
<table>
<thead>
    <tr><td>**Value**</td><td>**Description**</td</tr>
</thead>
<tbody>
    <tr><td>type</td><td>4</td></tr>
    <tr><td>response</td><td>File path</td></tr>
</tbody>
</table>


### File commands
File commands have `type=5` and will reply with the content of a specific file.
<table>
<thead>
    <tr><td>**Value**</td><td>**Description**</td</tr>
</thead>
<tbody>
    <tr><td>type</td><td>5</td></tr>
    <tr><td>trigger</td><td>The word that activates the command _(case insensitive)_</td></tr>
    <tr><td>response</td><td>File path</td></tr>
    <tr><td>defaultResponse</td><td>Message to send if the file is empty</td></tr>
    <tr><td>_adminOnly_</td><td>If 1, only admins will be able to trigger that command. _Optional_</td></tr>
    <tr><td>_reply_</td><td>If 1, the user who triggered the command will be notified.  _Optional_</td></tr>
</tbody>
</table>


## Examples
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
