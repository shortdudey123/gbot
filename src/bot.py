#!/usr/bin/env python
# =============================================================================
# file = bot.py
# description = IRC bot
# author = GR <https://github.com/shortdudey123>
# create_date = 2014-07-09
# mod_date = 2014-07-09
# version = 0.1
# usage = called as a class
# notes =
# python_ver = 2.7.6
# =============================================================================

import irc
import datetime


class IRCBot:
    """
    Takes in args to use for interacting with an IRC server
    """

    def __init__(self, server, nick, port=6667, realName='', identify='', debug=False, connectDelay=2):
        """
        Initialize the IRC server object

        Args:
            self (object): this python object instance
            server (str): DNS name or IP of IRC server to connect to
            nick (str): IRC nick to use
            port (int): port number that the IRC server runs on
            realName (str, optional): real name to send to the server, uses the nick by default
            identify (str, optional): nickserv password
            debug (boolean, optional): enable debug printing
            connectDelay (int, optional): number of seconds to wait for the IRC server to repond when connecting

        Returns:
            None

        Raises:
            None
        """
        self.debug = debug
        self.bot = irc.IRCClient(server, nick, port, realName, identify, debug, connectDelay)

    def run(self):
        """
        Run the bot

        Args:
            self (object): this python object instance

        Returns:
            None

        Raises:
            None
        """
        connectData = self.bot.connectToServer()

        for data in connectData:
            print data
            print "~~~~~~"

        while True:
            data = self.bot.getData()
            now = datetime.datetime.now()
            print now
            print data

        return

if __name__ == "__main__":
    filename = __file__.split('.')[0]
    help(filename)