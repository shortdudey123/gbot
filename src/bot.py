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

    def __init__(self, server, nick, port=6667, realName='', identify='', connectDelay=2, debug=False, ircDebug=False):
        """
        Initialize the IRC server object

        Args:
            server (str): DNS name or IP of IRC server to connect to
            nick (str): IRC nick to use
            port (int): port number that the IRC server runs on
            realName (str, optional): real name to send to the server, uses the nick by default
            identify (str, optional): nickserv password
            connectDelay (int, optional): number of seconds to wait for the IRC server to repond when connecting
            debug (boolean, optional): enable debug printing for bot side
            ircDebug (boolean, optional): enable debug printing for irc side

        Returns:
            None

        Raises:
            None
        """
        self.debug = debug
        self.bot = irc.IRCClient(server, nick, port, realName, identify, ircDebug, connectDelay)

    def run(self):
        """
        Run the bot

        Args:
            None

        Returns:
            None

        Raises:
            None
        """
        splitLinesLeftover = ''
        connectData = self.bot.connectToServer()

        for data in connectData:
            lines, splitLinesLeftover = splitLines(data, splitLinesLeftover)
            for line in lines:
                print line
                print "~~~~~~"

        while True:
            data = self.bot.getData()
            now = datetime.datetime.now()
            print now

            lines, splitLinesLeftover = splitLines(data, splitLinesLeftover)
            for line in lines:
                print line
                print "~~~~~~"

        return

    def splitLines(self, lines, leftover=''):
        """
        Splits up the data received into lines

        Note:
            Based on readNetworkLoop method by IsaacG
            https://github.com/IsaacG/python-projects/blob/master/ircbot/irc.py

        Args:
            lines (str): string of lines seperated by '\n'

        Returns:
            retLines (list): list of the seperated lines
            leftover (str): left over that was not part of a complete line

        Raises:
            None
        """
        retLines = []

        for line in lines.splitlines(True):
            if line[-2:] == '\r\n':
                line = line.rstrip('\r\n')
                line = '{0}{1}'.format(leftover, line)
                leftover = ''
                retLines.append(line)
            else:
                leftover = line

        return retLines, leftover

    def parseLine(self, line):
        pass

if __name__ == "__main__":
    filename = __file__.split('.')[0]
    help(filename)