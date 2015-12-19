import socket
import configparser
import sys
import os
import urllib.request

class config:
    config = configparser.ConfigParser()
    default = True      # if true, we have generated a default config.ini

    # Check if config.ini exists and load/generate it
    def __init__(self):
        if os.path.isfile("config.ini"):
            # config.ini found, load it
            self.config.read("config.ini")
            self.default = False
        else:
            # config.ini not found, generate a default one
            self.generateDefaultConfig()
            self.default = True

    # Check if config.ini has all needed the keys
    def checkConfig(self):
        try:
            # Try to get all the required keys
            self.config.get("auth","host")
            self.config.get("auth","port")
            self.config.get("auth","username")
            self.config.get("auth","password")
            self.config.get("auth","channel")
            self.config.get("auth","timeout")
            self.config.get("chat","startMessage")
            self.config.get("chat","botAdmins")
            self.config.get("debug","showServerOutput")
            self.config.get("debug","showDebugMessages")
            return True
        except:
            return False

    # Generate a default config.ini
    def generateDefaultConfig(self):
        # Open config.ini in write mode
        f = open("config.ini", "w")

        # Set keys to config object
        self.config.add_section("auth")
        self.config.set("auth", "host", "irc.twitch.tv")
        self.config.set("auth", "port", "6667")
        self.config.set("auth", "username", "YOUR_TWITCH_BOT_USERNAME")
        self.config.set("auth", "password", "YOUR_TWITCH_BOT_OAUTH_TOKEN")
        self.config.set("auth", "channel", "YOUR_TWITCH_CHANNEL")
        self.config.set("auth", "timeout", "2")

        self.config.add_section("chat")
        self.config.set("chat", "startMessage", "Hi! I'm Kirotuso, a Twitch chat bot! Type '!ping' to test me :)")
        self.config.set("chat", "botAdmins", "admin1,admin2")

        self.config.add_section("debug")
        self.config.set("debug", "showServerOutput", "0")
        self.config.set("debug", "showDebugMessages", "0")

        # Write ini to file and close
        self.config.write(f)
        f.close()

    # Check if a user is a bot admin
    def isAdmin(self, who):
        return who in self.config["chat"]["botAdmins"].split(",")

    # Print a debug message if they're enabled
    def debugMessage(self, message):
        if int(self.config["debug"]["showDebugMessages"]) == 1: print(message)

class commands:
    commands = configparser.ConfigParser()
    fileHooks = {}
    default = True      # if true, we have generated a default commands.ini

    # Check if commands.ini exists and load/generate it
    def __init__(self):
        if os.path.isfile("commands.ini"):
            # Read commands.ini
            self.commands.read("commands.ini")

            # Set default keys
            self.setDefaults()

            # Update filehooks
            self.setFileHooks()
            self.default = False
        else:
            # Can't find commands.ini, generate a default one
            self.generateDefaultCommands()
            self.default = True

    # Set default values
    def setDefaults(self):
        self.commands.set("DEFAULT","type","1")
        self.commands.set("DEFAULT","trigger","")
        self.commands.set("DEFAULT","response","")
        self.commands.set("DEFAULT","defaultResponse","")
        self.commands.set("DEFAULT","reply","0")
        self.commands.set("DEFAULT","period","-1")
        self.commands.set("DEFAULT","adminOnly","0")

    # Generate a default commands.ini
    def generateDefaultCommands(self):
        # Open commands.ini in write mode
        f = open("commands.ini", "w")

        # Set keys to cmd object
        self.commands.add_section("cmdPing")
        self.commands.set("cmdPing","type","1")
        self.commands.set("cmdPing","trigger","!ping")
        self.commands.set("cmdPing","response","Pong!")

        # Write ini to file and close
        self.commands.write(f)
        f.close()

    # Update fileHooks list
    def setFileHooks(self):
        # Clear current fileHooks
        self.fileHooks.clear()

        # Loop through all commands, serch for fileHooks and add them
        for i in self.commands:
            if int(self.commands[i]["type"]) == 4:
                self.fileHooks[i] = open(self.commands[i]["response"], "r").read()

    # Reload commands.ini, default keys and fileHooks
    def reloadCommands(self):
        self.commands.clear()
        self.commands.read("commands.ini")
        self.commands.setDefaults()
        self.setFileHooks()


class bot:
    __socket = socket.socket()
    host = None
    port = None
    username = None
    password = None
    channel = None

    # Instantiate a new bot
    def __init__(self, __host, __port, __username, __password, __channel, __timeout):
        self.host = __host
        self.port = __port
        self.username = __username
        self.password = __password
        self.channel = __channel
        self.sentMessages = 0
        self.receivedMessages = 0
        self.__socket.settimeout(__timeout)

    # Send a tcp packet to the server
    def sendToServer(self, message, encoding="UTF-8"):
        self.__socket.send(bytes(message+"\r\n", encoding))

    # Connect to the server. Return True if connected
    def connect(self):
        try:
            self.__socket.connect((self.host, self.port))
            return True
        except:
            return False

    # Send IRC login packets
    def login(self):
        self.sendToServer("PASS "+self.password)
        self.sendToServer("NICK "+self.username)
        self.sendToServer("USER "+self.username)
        self.sendToServer("JOIN #"+self.channel)

    # Send a message to channel's chat
    def sendToChat(self, message, incrementMessages = True):
        # Send PRIVMSG packet
        self.sendToServer("PRIVMSG #"+self.channel+" :"+message)

        # Increment messages count if needed
        if incrementMessages: self.sentMessages+=1

    # Get server response
    def getResponse(self, lenght=4096):
        return self.__socket.recv(lenght).decode()

# Load settings
print("==> Loading settings")
conf = config()

# Check if we have generated a default config.ini, if so exit
if conf.default == True:
    print("[!] Couldn't find config.ini. A default config.ini has been generated in bot's folder. Please edit it and run the bot again.")
    sys.exit()

# If we haven't generated a default config.ini, check if it's valid
if conf.checkConfig() == False:
    print("[!] Invalid config file")
    sys.exit()
else:
    print("==> Settings loaded")

# Load commands.ini
print("==> Loading commands")
cmd = commands()

# Check if we have generated a default commands.ini, if so exit
if cmd.default == True:
    print("[!] Couldn't find command.ini. A default command.ini has been generated in bot's folder. Please edit it and run the bot again.")
    sys.exit()

# Ini files are valid, create a bot instance
print("==> Connecting to Twitch IRC server")
b = bot(conf.config["auth"]["host"], int(conf.config["auth"]["port"]), conf.config["auth"]["username"], conf.config["auth"]["password"], conf.config["auth"]["channel"], int(conf.config["auth"]["timeout"]))

# Connect to IRC server
if b.connect() == False:
    print("[!] Connection error. Please check your internet connection and config.ini file")
    sys.exit()

# Send login packets
print("==> Logging in")
b.login()

# Check login errors
response = b.getResponse();
if response.lower().find("error") != -1:
    print("[!] Login error. Please check your config.ini file")
    if conf.config["debug"]["showServerOutput"]: print("/r/n/r/n"+response)
    sys.exit()

# Send start message if needed
if conf.config["chat"]["startMessage"] != "":
    b.sendToChat(conf.config["chat"]["startMessage"])

# No errors, start the loop
print("==> Kirotuso is listening!")
while 1:
    # Debug message
    conf.debugMessage("==> Looping...")

    # Loop through all file hooks
    for i in cmd.fileHooks:
        try:
            # Get content of that file
            oldContent = cmd.fileHooks[i]
            newContent = open(cmd.commands[i]["response"], "r").read()

            # If content is different, update fileHook and send message
            if newContent != oldContent and newContent != "":
                cmd.fileHooks[i] = newContent
                print("==> Content changed, sending new content to chat ("+i+")")
                b.sendToChat(newContent)
        except:
            print("[!] Error while reading file ("+i+")")

    try:
        # Get new packets
        r = b.getResponse().lower()

        # Check if we have new packets
        # TODO: this if is probably useless
        if r != None:
            # Make sure this is a PRIVMSG packet
            if r.find("privmsg") != -1:
                # Increment received messages
                b.receivedMessages+=1

                # Get who has sent the message
                rFrom = r.split("!")[0][1:]

                # Set final message to empty
                message=""

                # Check if that message triggered an interal command
                if r.find("!reloadcmd") != -1:
                    # Reload commands (!reloadCmd)
                    b.sendToChat("Commands reloaded!")
                    cmd.reloadCommands()
                # elif r.find("!othercommand") != -1: ...

                # Check if that message triggered a custom command
                # Loop through all commands
                for i in cmd.commands:
                    # Get command data
                    cmdName = i
                    cmdType = int(cmd.commands[i]["type"])
                    cmdTrigger = cmd.commands[i]["trigger"].lower()
                    cmdResponse = cmd.commands[i]["response"]
                    cmdDefaultResponse = cmd.commands[i]["defaultResponse"]
                    cmdReply = int(cmd.commands[i]["reply"])
                    cmdPeriod = int(cmd.commands[i]["period"])
                    cmdAdminOnly = int(cmd.commands[i]["adminOnly"])

                    # Make sure the command has valid response and period (default for non-periodic commands is -1)
                    if cmdResponse != "" and cmdPeriod != 0:
                        if cmdType == 1:
                            # Normal command
                            if r.find(cmdTrigger) != -1:
                                if cmdAdminOnly == 1 and not conf.isAdmin(rFrom):
                                    print("==> "+rFrom+" triggered a simple admin command, but he's not an admin")
                                else:
                                    print("==> "+rFrom+" triggered a simple command ("+cmdName+")")
                                    message=cmdResponse
                                    if cmdReply == 1: message=rFrom+" >> "+message

                        elif cmdType == 2:
                            # Periodic command
                            if b.receivedMessages%cmdPeriod == 0:
                                print("==> Sending periodic command ("+cmdName+")")
                                message=cmdResponse

                        elif cmdType == 3:
                            # API command
                            if r.find(cmdTrigger) != -1:
                                try:
                                    # Get API content and send it
                                    req = urllib.request.Request(cmdResponse,data=None,headers={'User-Agent': 'Mozilla/5.0'})
                                    apiResponse = urllib.request.urlopen(req).read().decode("UTF-8")
                                    message=apiResponse
                                    if cmdReply == 1: message=rFrom+" >> "+message
                                    print("==> "+rFrom+" triggered an API command ("+cmdName+")")
                                except:
                                    print("[!] Error while requesting API command ("+cmdName+")")

                        elif cmdType == 5:
                            # File read command
                            if r.find(cmdTrigger) != -1:
                                try:
                                    # Read file content and send it
                                    print("==> "+rFrom+" triggered a file read command ("+cmdName+")")
                                    content = open(cmdResponse, "r").read()

                                    # If content is empty, send default response
                                    if content == "":
                                        message = cmdDefaultResponse
                                    else:
                                        message = content

                                    if cmdReply == 1: message=rFrom+" >> "+message
                                except:
                                    print("[!] Error while reading file ("+i+")")

                # Send final message if needed
                if message != "":
                    b.sendToChat(message)

            # Print received packet if needed
            if int(conf.config["debug"]["showServerOutput"]) == 1:
                print(r, end="")
    except:
        pass
