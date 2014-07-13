#!/usr/bin/env python
# =============================================================================
# file = moduleInfo.py
# description = gbot module
# author = GR <https://github.com/shortdudey123>
# create_date = 2014-07-12
# mod_date = 2014-07-12
# version = 0.1
# usage = loaded by gbot
# notes =
# python_ver = 2.7.6
# =============================================================================

adminOnly = True
commandName = 'moduleInfo'
version = 0.1

def execModule(channel, message, nick, botSelf):
	retCommands = []
	botSelf.bot.sendMessage(channel, '<module name>: <command> <admin only> <version>'.format(channel, nick))
	for module in botSelf.loadedModules.keys():
		botSelf.bot.sendMessage(channel, '{0}: {1} {2} {3}'.format(botSelf.loadedModules[module]['module'], module, botSelf.loadedModules[module]['admin'], 'XXXX'))
	return retCommands

if __name__ == "__main__":
    filename = __file__.split('.')[0]
    help(filename)