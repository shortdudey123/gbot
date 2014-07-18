# gbot

## Introduction

IRC bot that can load custom command modules

The bot handles most types of IRC messages including INVITE, NOTICE, ERROR, KICK, and PRIVMSG.

## Setup

1. Close this repo
2. Modify gbot.py in the root of the repo to your liking

Note: no packages need to be installed.  Everything used is in stdlib.

## Sample config

	import src.bot as bot

	if __name__ == "__main__":
	    myBot = bot.IRCBot(server="irc.example.com", nick="myBot", port=6667, realName='myBot', identify='myBotPassword', debug=True, connectDelay=4, identVerifyCall='ACC')
	    myBot.setDefaultChannels({'#myBot': 'key', '#myBot2': ''})
	    myBot.addAdmin("myBotAdminNick", True)
	    myBot.loadModules(['coreVersion', 'moduleInfo', 'help'])
	    myBot.run()

## Running the Bot

Run the bot by calling `python gbot.py` in the root of the repo.

## Using the Bot

By default the only commands the bot will support is `quit` and `loadModule`.  
To load modules on startup, call `.loadModules(['mod1', 'mod2'])` before running the bot.
Loading modules after the bot is started can be done with a command in a channel or via sidechat. `bot: loadModule <module name>`

Note: The module name used to load the module is based on the .py filename and can be different than the command used to actually used the module.

All commands must be prefixed with the bot's name and a colon.  Example: `myBot: help`

Every module has it's own help message.  Example: `mybot: help version`

## Writing a module

A module can do anything that you want.  If you have a module that you thing should be part of the default modules included in the repo, feel free to let me know! (see the questions section)

### Skeleton Code

	adminOnly = True
	commandName = 'command'
	version = 0.1
	help = """
	Help Message
	Usage: {0} <options>
	Admin Only: {1}
	Version: {2}
	Note: any notes
	""".format(commandName, adminOnly, version)

	def execModule(channel, message, nick, botSelf):
	    retCommands = []

	    # insert code here

	    return retCommands

	if __name__ == "__main__":
	    filename = __file__.split('.')[0]
	    help(filename)

### Skeleton Code Explained

adminOnly - can restrict the module to only allow admins to call it

commandName - the name you will use to call the module (generally the same as the filename)

version - version number

help - help message displayed when help module is called

channel - source channel of the message (source nick if sidechat)

message - exactly what is sent on IRC minus the bot name.  (EX: `myBot: help version` would be `help version`)

nick - source nick of the command (will be same as channel if source was a side chat)

botSelf - reference to the bot instance (used to call bot commands like sending a message or accessing variables)

### Things to go inside the module

Send a message to a channel: `botSelf.bot.sendMessage(channel, 'Hi {0}!'.format(nick))`

Send a message to a channel and highlight a nick: `botSelf.bot.sendMessage(channel, 'Hi!'.format(nick), nick)`

Send a message to a nick: `botSelf.bot.sendMessage(nick, 'Hi!')`

Join a channel: `botSelf.joinChannel(channel, optionalKey)`

Put something in the log: `botSelf.log(message, optionalLevel)`

Get bot nick: `botSelf.bot.getNick()`

## Other Notes

The bot will auto rejoin a channel if it is kicked and the channel is one its defaults.

## Questions?

Drop by [##gbot on Freenode](http://webchat.freenode.net/?channels=##gbot)