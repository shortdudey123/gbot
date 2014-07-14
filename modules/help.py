#!/usr/bin/env python
# =============================================================================
# file = help.py
# description = gbot module
# author = GR <https://github.com/shortdudey123>
# create_date = 2014-07-12
# mod_date = 2014-07-12
# version = 0.1
# usage = loaded by gbot
# notes =
# python_ver = 2.7.6
# =============================================================================

adminOnly = False
commandName = 'help'
version = 0.1

def execModule(channel, message, nick, botSelf):
	retCommands = []
	botSelf.bot.sendMessage(channel, 'I am an instance of gbot (https://github.com/shortdudey123/gbot)')
	return retCommands

if __name__ == "__main__":
    filename = __file__.split('.')[0]
    help(filename)