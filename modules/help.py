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
version = 0.2
help = """
Gets help for the modules
Usage: {0} <command>
Admin Only: {1}
Version: {2}
""".format(commandName, adminOnly, version)

def execModule(channel, message, nick, botSelf):
    retCommands = []
    if len(message.split()) == 1:
        commands = ', '.join(botSelf.loadedModules.keys())

        botSelf.bot.sendMessage(channel, 'I am an instance of gbot (https://github.com/shortdudey123/gbot)')
        botSelf.bot.sendMessage(channel, 'Commands (built in): loadModule, quit')
        botSelf.bot.sendMessage(channel, 'Commands (modules): {0}'.format(commands))
        botSelf.bot.sendMessage(channel, 'For help on the commands: help <command>')
        botSelf.bot.sendMessage(channel, 'Note: all commands must be preceded by {0}:'.format(botSelf.bot.nick))
    elif len(message.split()) == 2 and message.split()[1] in botSelf.loadedModules.keys():
        for line in botSelf.loadedModules[message.split()[1]]['help'].split('\n'):
            botSelf.bot.sendMessage(channel, line)
    return retCommands

if __name__ == "__main__":
    filename = __file__.split('.')[0]
    help(filename)