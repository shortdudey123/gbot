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
        self.channels = {}

    def log(self, message, level="INFO"):
        """
        Logs the given message

        Args:
            message (str): message to log
            level (str, optional): log level

        Returns:
            None

        Raises:
            None
        """
        now = datetime.datetime.now()
        print "{0} [{1}] {2}".format(now, level, message)
        return

    def setDefaultChannels(self, channels):
        """
        Set the default channels to join on startup

        Args:
            channels (dict): channels with keys (i.e. {'channel1': '', 'channel2': 'key'})

        Returns:
            None

        Raises:
            None
        """
        self.log("Set default channels to: {0}".format(channels))
        self.channels = channels
        return

    def joinDefaultChannels(self):
        """
        Join the default channels

        Args:
            None

        Returns:
            None

        Raises:
            None
        """
        self.log("Joining default channels")
        for channel in self.channels.keys():
            self.joinChannel(channel, self.channels[channel])
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

    def pong(self, server):
        """
        Passes on the server to pong to

        Args:
            server (str): name of server to pong to

        Returns:
            None

        Raises:
            None
        """
        self.bot.sendPong(server)
        return

    def joinChannel(self, channel, key=''):
        """
        Join the given channel

        Args:
            channel (str): channel name
            key (str, optional): key for the channel

        Returns:
            None

        Raises:
            None
        """
        self.bot.joinChannel(channel, key)
        self.log("Joining {0}".format(channel))

    def parseLine(self, line):
        """
        Parses the lines received from the server

        Args:
            line (str): string data containing a single line from the server

        Returns:
            None

        Raises:
            None
        """
        self.log(line)

        if len(line.split()) == 2 and line.split()[0] == "PING":
            self.bot.sendPong(line.split()[1])
            self.log("Sending pong")

        return

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
            lines, splitLinesLeftover = self.splitLines(data, splitLinesLeftover)
            for line in lines:
                self.parseLine(line)

        self.joinDefaultChannels()

        while self.bot.isConnected():
            data = self.bot.getData()

            lines, splitLinesLeftover = self.splitLines(data, splitLinesLeftover)
            for line in lines:
                self.parseLine(line)

        log("{0} has shutdown".format(self.nick))
        return

if __name__ == "__main__":
    filename = __file__.split('.')[0]
    help(filename)