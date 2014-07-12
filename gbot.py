#!/usr/bin/env python
# =============================================================================
# file = gbot.py
# description = IRC bot
# author = GR <https://github.com/shortdudey123>
# create_date = 2014-07-09
# mod_date = 2014-07-09
# version = 0.1
# usage = called as a class
# notes =
# python_ver = 2.7.6
# =============================================================================

import src.bot as bot


if __name__ == "__main__":
    gbot = bot.IRCBot(server="chat.freenode.com", nick="grbot", port=6667, realName='gbot', identify='', debug=True, connectDelay=4, identVerifyCall='ACC')
    gbot.setDefaultChannels({'##gbot': ''})
    gbot.addAdmin("shortdudey123")
    gbot.loadModule("opme")
    gbot.run()