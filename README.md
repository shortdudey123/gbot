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