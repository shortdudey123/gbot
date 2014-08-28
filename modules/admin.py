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
commandName = 'admin'
version = 0.1
help = """
View and modify the list of admins for this bot.
Usage: {0} <list | add nick | del nick>
Admin Only: {1}
Version: {2}
Note: 
""".format(commandName, adminOnly, version)

def execModule(channel, message, nick, botSelf):
    retCommands = []
    if len(message.split()) == 2 and message.split()[1].lower() == 'list':
        botSelf.bot.sendMessage(channel, 'Admins: {0}'.format(' '.join(botSelf.admins)))
        botSelf.bot.sendMessage(channel, 'Owners: {0}'.format(' '.join(botSelf.owners)))
    elif len(message.split()) == 3:
        adminNick = message.split()[2]
        if message.split()[1].lower() == 'add':
            if botSelf.addAdmin(adminNick):
                botSelf.bot.sendMessage(channel, 'Added an admin: {0}'.format(adminNick))
            else:
                botSelf.bot.sendMessage(channel, '{0} is already an admin!'.format(adminNick))
        if message.split()[1].lower() == 'del':
            try:
                delMsg = botSelf.deleteAdmin(adminNick)
                botSelf.bot.sendMessage(channel, '{0}'.format(delMsg))
            except Exception, e:
                botSelf.bot.sendMessage(channel, '{0}'.format(e))

    return retCommands

if __name__ == "__main__":
    filename = __file__.split('.')[0]
    help(filename)
