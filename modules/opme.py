#!/usr/bin/env python
# =============================================================================
# file = opme.py
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
commandName = 'opme'
version = 0.1
help_msg = """
Gives the requestor op
Usage: {0}
Admin Only: {1}
Version: {2}
Note: this requires the bot to be op in the channel
""".format(commandName, adminOnly, version)


def execModule(channel, message, nick, botSelf):
    retCommands = []
    botSelf.bot.sendMessage('ChanServ', 'op {0} {1}'.format(channel, nick))
    botSelf.log("{0} for {1} in {2}".format(message, nick, channel))
    return retCommands

if __name__ == "__main__":
    filename = __file__.split('.')[0]
    help(filename)
