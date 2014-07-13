#!/usr/bin/env python
# =============================================================================
# file = coreVersion.py
# description = gbot module
# author = GR <https://github.com/shortdudey123>
# create_date = 2014-07-13
# mod_date = 2014-07-13
# version = 0.1
# usage = loaded by gbot
# notes =
# python_ver = 2.7.6
# =============================================================================

adminOnly = False
commandName = 'version'
version = 0.1

def execModule(channel, message, nick, botSelf):
	retCommands = []
	botSelf.bot.sendMessage(channel, 'I am running core version {0}'.format(botSelf.version))
	return retCommands

if __name__ == "__main__":
    filename = __file__.split('.')[0]
    help(filename)