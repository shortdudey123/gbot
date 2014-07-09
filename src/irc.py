#!/usr/bin/env python
# =============================================================================
# file = irc.py
# description = interact with an IRC server
# author = GR <https://github.com/shortdudey123>
# create_date = 2014-07-08
# mod_date = 2014-07-08
# version = 0.1
# usage = called as a class
# notes =
# python_ver = 2.7.6
# =============================================================================
"""
irc.py
"""

import socket
import time


class IRCServer:
    """
    Takes in args to use to for interacting with an IRC server
    """

    def __init__(self, server, nick, port=6667, realName='', identify='', debug=False, connectDelay=2):
        self.server = server
        self.port = port
        self.nick = nick
        self.channels = {}
        self.debug = debug
        self.identify = identify
        self.connectDelay = connectDelay
        self.realName = realName
        
        if realName == '':
            self.realName = self.nick

        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connectToServer(self):
        self.irc.connect((self.server,self.port))

        # need to wait for the server to respond
        time.sleep(self.connectDelay)

        if self.debug:
            print self.getData()
            print "~~~~~~~~~~~~~~"

        self.irc.send("USER {0} * 0 :{1}\n".format(self.nick, self.realName))
        self.irc.send("NICK {0}\n".format(self.nick))

        if self.identify != '':
            self.irc.send("PRIVMSG nickserv :identify {0} {1}\r\n".format(self.nick, self.identify))

        # need to wait for the server to respond
        time.sleep(self.connectDelay)

        if self.debug:
            print self.getData()
            print "~~~~~~~~~~~~~~"

        return

    def disconnectFromServer(self):
        self.irc.send('QUIT\n')
        self.irc.close()
        return

    def sendMessage(self, channel, message, nick=''):
        if nick == '':
            self.irc.send("PRIVMSG {0} : {1}\n".format(channel, message))
        else:
            self.irc.send("PRIVMSG {0} : {1}: {2}\n".format(channel, nick, message))

        if self.debug:
            print "*** Sent message in {0} ***".format(channel)
            print self.getData()
            print "~~~~~~~~~~~~~~"

        return

    def joinChannel(self, channel, key=''):
        self.irc.send("JOIN {0} {1}\n".format(channel, key))
        return

    def setDebug(self, debug):
        self.debug = debug
        return

    def getData(self):
        # 16kb buffer allows for huge messages (i.e. MOTD)
        data = self.irc.recv(16384)
        return data

if __name__ == "__main__":
    className = IRCServer

    # print out docstrings
    if hasattr('__doc__'):
            print getattr('__doc__')
    if hasattr(getattr(className), '__doc__'):
            print getattr(getattr(className), '__doc__')
    for method in dir(className):
        if hasattr(getattr(className, method), '__doc__'):
            print getattr(getattr(className, method), '__doc__')