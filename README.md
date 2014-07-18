gbot
====

Introduction
------------

IRC bot that can load custom command modules

Setup
-----

1. Close this repo
2. Modify gbot.py in the root of the repo to your liking

Note: no packages need to be installed.  Everything used is in stdlib.

Sample config
-------------

	import src.bot as bot

	if __name__ == "__main__":
	    myBot = bot.IRCBot(server="irc.example.com", nick="myBot", port=6667, realName='myBot', identify='myBotPassword', debug=True, connectDelay=4, identVerifyCall='ACC')
	    myBot.setDefaultChannels({'#myBot': ''})
	    myBot.addAdmin("myBotAdminNick", True)
	    myBot.loadModules(['coreVersion', 'moduleInfo', 'help'])
	    myBot.run()

Running the Bot
---------------

Run the bot by calling `python gbot.py` in the root of the repo.

Using the Bot
-------------

By default the only commands the bot will support is `quit` and `loadModule`.  
To load modules on startup, call `.loadModules(['mod1', 'mod2'])` before running the bot.
Loading modules after the bot is started can be done with a command in a channel or via sidechat. `bot: loadModule <module name>`

Note: The module name used to load the module is based on the .py filename and can be different than the command used to actually used the module.

Questions?
----------

Drop by [##gbot on Freenode](http://webchat.freenode.net/?channels=##gbot)