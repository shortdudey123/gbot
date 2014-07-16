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

__IRC_LIB_VERSION__ = 0.1

class IRCClient:
    """
    Takes in args to use for interacting with an IRC server
    """

    def __init__(self, server, nick, port=6667, realName='', identify='', debug=False, connectDelay=2, identVerifyCall=''):
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
        # greb args
        self.server = server
        self.port = port
        self.nick = nick
        self.debug = debug
        self.identify = identify
        self.connectDelay = connectDelay
        self.realName = realName
        self.actualServer = self.server
        self.identVerifyCall = identVerifyCall

        if realName == '':
            self.realName = self.nick

        # set other defaults
        self.connected = False
        self.channelPrefixes = ['#', '!', '&', '+']
        self.soccketBufferSizeDefault = 16384
        self.soccketBufferSize = self.soccketBufferSizeDefault

        # create the socket
        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def getVersion(self):
        """
        Gets the version of the IRC lib

        Args:
            None

        Returns:
            version (int): version number of IRC lib

        Raises:
            None
        """
        return __IRC_LIB_VERSION__

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

    def _setSocketBufferSize(self, size=''):
        """
        Disconnect from the IRC server

        Args:
            size (int, optional): change the buffer size, change to default if not set

        Returns:
            boolean: success or failure of change

        Raises:
            None
        """
        if size == '':
            self.soccketBufferSize = self.soccketBufferSizeDefault
        elif type(size) == int:
            self.soccketBufferSize = size
        else:
            return False
        return True

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

    def sendMessageInvite(self, channel, nick):
        """
        Send an channel invite to the given nick

        Args:
            channel (str): channel to invite the nick to
            nick (str): nick to invite

        Returns:
            None

        Raises:
            None
        """
        self.irc.send("INVITE {0} {1}\n".format(nick, channel))
        return

    def sendMessageKick(self, channel, nick, reason=''):
        """
        Kick the nick from the given channel

        Args:
            channel (str): channel to invite the nick to
            nick (str): nick to invite
            reason (str, optional): kick message

        Returns:
            None

        Raises:
            None
        """
        if reason == '':
            self.irc.send("KICK {0} {1}\n".format(channel, nick))
        else:
            self.irc.send("KICK {0} {1} :{2}\n".format(channel, nick, reason))
        return

    def getNames(self, channel='', target=''):
        """
        Kick the nick from the given channel

        Args:
            channel (str, optional): channels to get names for (can be a comma seperated list of channels)
            target (str, optional): send to a specific server

        Returns:
            None

        Raises:
            None
        """
        retData = ''
        if channel == '':
            self._setSocketBufferSize(self.soccketBufferSizeDefault*10)
            self.irc.send("NAMES\n")
            retData = self.getData()
            self._setSocketBufferSize()
        else:
            if target == '':
                self.irc.send("NAMES {0}\n".format(channel))
                retData = self.getData()
            else:
                self.irc.send("NAMES {0} {1}\n".format(channel, target))
                retData = self.getData()
        return retData

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
        self.irc.send("{0}\n".format(message))

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

    def partChannel(self, channel, reason=''):
        """
        Join a given channel

        Args:
            channel (str): channel to part
            reason (str, optional): part message

        Returns:
            None

        Raises:
            None
        """
        if reason == '':
            self.irc.send("PART {0}\n".format(channel))
        else:
            self.irc.send("PART {0} :{1}\n".format(channel, reason))
        return

    def setChannelMode(self, channel, modes, param=''):
        """
        Set the mode for the given channel

        Args:
            channel (str): channel to part
            modes (str): +/- modes to change
            param (str, optional): parameters for the mode change (i.e. a key for +k)

        Returns:
            None

        Raises:
            None
        """
        if param == '':
            self.irc.send("MODE {0} {1}\n".format(channel, mode))
        else:
            self.irc.send("MODE {0} {1} {2}\n".format(channel, mode, param))
        return

    def setChannelTopic(self, channel, topic):
        """
        Set the topic for the given channel

        Args:
            channel (str): channel to part
            topic (str): new topic for the channel

        Returns:
            None

        Raises:
            None
        """
        self.irc.send("TOPIC {0} {1}\n".format(channel, topic))
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
        data = self.irc.recv(self.soccketBufferSize)
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

    def isIdentified(self, nick):
        """
        Gives the connection status of the socket

        Args:
            nick (str): nick to check IDENTIFY on

        Returns:
            str: True for connected, False for diconnected

        Raises:
            Exception: if NickServ is queried and the status code is not an int

        Note:
            This is based on info from http://stackoverflow.com/questions/1682920/determine-if-a-user-is-idented-on-irc

            The answer is in the form ACC :
                0 - account or user does not exist
                1 - account exists but user is not logged in
                2 - user is not logged in but recognized (see ACCESS)
                3 - user is logged in

            The answer is in the form STATUS :
                0 - no such user online or nickname not registered
                1 - user not recognized as nickname's owner
                2 - user recognized as owner via access list only
                3 - user recognized as owner via password identification
        """
        retIsIdentified = False
        statusCode = ''

        # no call specified so assume no idenitify validation is possible
        if self.identVerifyCall == '':
            retIsIdentified = True

        # validation is possible
        else:

            if self.identVerifyCall == 'ACC':
                data = self.sendMessageSpecial("PRIVMSG NickServ ACC {0}".format(nick), needDataBack = True)
                if len(data) >= 5:
                    statusCode = data.split()[5]

            elif self.identVerifyCall == 'STATUS':
                data = self.sendMessageSpecial("PRIVMSG NickServ STATUS {0}".format(nick), needDataBack = True)
                print 'data: {0}'.format(data)
                if len(data) >= 4:
                    statusCode = data.split()[3]
                    print 'statusCode: {0}'.format(statusCode)

            try:
                if int(statusCode) == 3:
                    retIsIdentified = True
            except Exception:
                raise Exception("Unabled to read the status code of {0}".format(nick))

        return retIsIdentified

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