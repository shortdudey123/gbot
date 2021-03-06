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
help_msg = """
Displays the version of the bot core
Usage: {0}
Admin Only: {1}
Version: {2}
""".format(commandName, adminOnly, version)


def execModule(channel, message, nick, botSelf):
    retCommands = []
    botSelf.bot.sendMessage(channel, 'Core Versions:')
    botSelf.bot.sendMessage(channel, 'Bot - {0}'.format(botSelf.getVersion()))
    botSelf.bot.sendMessage(channel, 'IRC - {0}'.format(botSelf.bot.getVersion()))
    botSelf.log("{0} for {1} in {2}".format(message, nick, channel))
    return retCommands

if __name__ == "__main__":
    filename = __file__.split('.')[0]
    help(filename)
