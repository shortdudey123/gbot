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
commandName = 'setTopic'
version = 0.1
help_msg = """
Sets the topic of the channel.  Omit the topic param to clear the topic.
Usage: {0} <topic>
Admin Only: {1}
Version: {2}
Note: this requires the bot to be op in the channel
""".format(commandName, adminOnly, version)


def execModule(channel, message, nick, botSelf):
    retCommands = []
    if len(message.split()) >= 2:
        botSelf.bot.setChannelTopic(channel, '{0}'.format(' '.join(message.split()[1:])))
    elif len(message.split()) == 1:
        botSelf.bot.setChannelTopic(channel)
    return retCommands

if __name__ == "__main__":
    filename = __file__.split('.')[0]
    help(filename)
