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

import socket
import time


class IRCClient:
    """
    Takes in args to use for interacting with an IRC server
    """

    def __init__(self, server, nick, port=6667, realName='', identify='', debug=False, connectDelay=2):
        """
        Initialize the IRC server object

        Args:
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
        self.server = server
        self.port = port
        self.nick = nick
        self.debug = debug
        self.identify = identify
        self.connectDelay = connectDelay
        self.realName = realName
        self.connected = False
        self.actualServer = self.server
        self.channelPrefixes = ['#', '!', '&', '+']
        
        if realName == '':
            self.realName = self.nick

        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connectToServer(self):
        """
        Connect to the IRC server

        Args:
            None

        Returns:
            retData (list): data received from the server while connecting

        Raises:
            None
        """
        retData = []
        self.irc.connect((self.server,self.port))

        self.connected = True

        # need to wait for the server to respond
        time.sleep(self.connectDelay)

        data = self.getData()
        retData.append(data)

        if self.debug:
            print data
            print "~~~~~~~~~~~~~~"

        self.irc.send("USER {0} * 0 :{1}\n".format(self.nick, self.realName))
        self.irc.send("NICK {0}\n".format(self.nick))

        if self.identify != '':
            self.irc.send("PRIVMSG nickserv :identify {0} {1}\r\n".format(self.nick, self.identify))

        # need to wait for the server to respond
        time.sleep(self.connectDelay)

        data = self.getData()
        retData.append(data)

        if self.debug:
            print data
            print "~~~~~~~~~~~~~~"

        return retData

    def disconnectFromServer(self):
        """
        Disconnect from the IRC server

        Args:
            None

        Returns:
            None

        Raises:
            None
        """
        self.irc.send('QUIT\n')
        self.irc.close()
        self.connected = False
        return

    def sendMessage(self, channel, message, nick=''):
        """
        Send a message in a given channel

        Args:
            channel (str): channel to send the message in
            message (str): message to send
            nick (str, optional): nick to prefix to the message for highlighting

        Returns:
            None

        Raises:
            None
        """
        if nick == '':
            self.irc.send("PRIVMSG {0} : {1}\n".format(channel, message))
        else:
            self.irc.send("PRIVMSG {0} : {1}: {2}\n".format(channel, nick, message))

        if self.debug:
            print "*** Sent message in {0} ***".format(channel)
            print self.getData()
            print "~~~~~~~~~~~~~~"

        return

    def sendMessageSpecial(self, message, needDataBack = False):
        """
        Send a message to the server that is not already defined

        Args:
            message (str): message to send to the server
            needDataBack (boolean, optional): set True is you need the response of the server

        Returns:
            str: string of the data reseived from the server

        Raises:
            None
        """
        retData = ''
        self.irc.send("PRIVMSG {0} : {1}\n".format(channel, message))

        if needDataBack:
            retData = self.getData()

        return retData

    def joinChannel(self, channel, key=''):
        """
        Join a given channel

        Args:
            channel (str): channel to join
            key (str, optional): key for the channel

        Returns:
            None

        Raises:
            None
        """
        self.irc.send("JOIN {0} {1}\n".format(channel, key))
        return

    def setDebug(self, debug):
        """
        Change debuging status

        Args:
            debug (boolean): enable or disable debug

        Returns:
            None

        Raises:
            None
        """
        self.debug = debug
        return

    def sendPong(self, server):
        """
        Send a pong message

        Args:
            server (str): name of server to pong to

        Returns:
            None

        Raises:
            None
        """
        self.irc.send("PONG {0}\n".format(server))
        return

    def getData(self):
        """
        Receive data from the IRC server

        Args:
            None

        Returns:
            str: Data received from the server

        Raises:
            None
        """
        # 16kb buffer allows for huge messages (i.e. MOTD)
        data = self.irc.recv(16384)
        if not data:
            self.connected = False
        return data

    def isConnected(self):
        """
        Gives the connection status of the socket

        Args:
            None

        Returns:
            str: True for connected, False for diconnected

        Raises:
            None
        """
        return self.connected

    def setActualServer(self, server):
        """
        Allows the overriding of the servername that the socket is connected to

        Note:
            This is needed since some server DNS names are CNAME's or contain multiple A records.
            This can be detected be looking at the first part of the MOTD
            (i.e. chat.freenode.com)

        Args:
            server (str): server name of the connection

        Returns:
            None

        Raises:
            None
        """
        self.actualServer = server
        return


    def getChannelPrefixes(self):
        """
        Gives the prefixes for channels

        Args:
            None

        Returns:
            list: list of single character prefixes

        Raises:
            None
        """
        return self.channelPrefixes

    def getNick(self):
        """
        Gives the nick used for IRC connection

        Args:
            None

        Returns:
            str: nick assigned to connection

        Raises:
            None
        """
        return self.nick


    def setChannelPrefixes(self, prefixes):
        """
        Override the prefixes for channels

        Args:
            prefixes (list): list of prefixes

        Returns:
            None

        Raises:
            None
        """
        self.channelPrefixes = prefixes
        return

if __name__ == "__main__":
    filename = __file__.split('.')[0]
    help(filename)