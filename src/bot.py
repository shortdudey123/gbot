#!/usr/bin/env python
# =============================================================================
# file = bot.py
# description = IRC bot
# author = GR <https://github.com/shortdudey123>
# create_date = 2014-07-09
# mod_date = 2014-07-13
# version = 0.1
# usage = called as a class
# notes =
# python_ver = 2.7.6
# =============================================================================

# python standard
import datetime

# add one dir up to the path
import site
site.addsitedir("../")
del site

# custom imports
import irc
import modules

__CORE_VERSION__ = 0.1


class IRCBot(object):
    """
    Takes in args to use for interacting with an IRC server
    """

    def __init__(self, server, nick, port=6667, realName='', identify='', connectDelay=2, debug=False, ircDebug=False, identVerifyCall=''):
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
        self.bot = irc.IRCClient(server, nick, port, realName, identify, ircDebug, connectDelay, identVerifyCall)
        self.channels = {}
        self.admins = []
        self.loadedModules = {}
        self.owners = []

    def getVersion(self):
        """
        Gets the version of the bot core

        Args:
            None

        Returns:
            version (int): version number of bot core

        Raises:
            None
        """
        return __CORE_VERSION__

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

    def addAdmin(self, nick, owner=False):
        """
        Parses the PRIVMSG received from the server

        Args:
            nick (str): nick to add to admin list
            owner (boolean, optional): owner(s) of the bot (shoud not be removed from the admins list once set)

        Returns:
            boolean: False if nick is alrady in the list, otherwise true

        Raises:
            None
        """
        retAdminAdded = True
        if nick not in self.admins:
            self.admins.append(nick)
            self.log('Added admin: {0}'.format(nick))

            if owner:
                self.owners.append(nick)
                self.log('Added owner: {0}'.format(nick))
        else:
            retAdminAdded = False
            self.log('Add admin failed since the nick is already an admin: {0}'.format(nick))
        return retAdminAdded

    def deleteAdmin(self, nick):
        """
        Remove the given nick from the admin list

        Args:
            nick (str): nick to add to admin list
            owner (boolean, optional): owner(s) of the bot (shoud not be removed from the admins list once set)

        Returns:
            None

        Raises:
            None
        """
        # verify the nick is not an owner
        if nick in self.owners:
            self.log('Could not remove an admin since they are an owner: {0}'.format(nick))
            raise Exception("You can't remove an owner from the admin list!")
        else:
            try:
                self.admins.remove(nick)
                self.log('Removed admin: {0}'.format(nick))
            except ValueError, e:
                self.log('Could not remove an admin since they are not in the list: {0}'.format(nick))
                self.log(e)
                raise Exception("{0} is not an admin!".format(nick))
        return 'Removed {0} from the admin list'.format(nick)

    def isAdminAndIdent(self, nick):
        """
        Verifies an admin and their identity

        Args:
            nick (str): nick to verify

        Returns:
            int: 0 - not admin
                 1 - admin, but not ident
                 2 - admin, but can't validate ident
                 3 - admin and valid ident

        Raises:
            None
        """
        retCode = 0

        if nick in self.admins:
            try:
                if self.bot.isIdentified(nick):
                    retCode = 3
                else:
                    retCode = 1
            except Exception, e:
                self.log(e, level="ERROR")
                retCode = 2

        # if there is no admins set, then we can't determine who should do what so we should disable the admin side
        # Want all hell to break loose?? Change this from 0 to 3
        elif len(self.admins) == []:
            retCode = 0

        return retCode

    def adminCheckFailed(self, channel, nick, adminCode):
        """
        Verifies an admin and their identity

        Args:
            nick (str): nick to verify

        Returns:
            int: 0 - not admin
                 1 - admin, but not ident
                 2 - admin, but can't validate ident
                 3 - admin and valid ident

        Raises:
            None
        """
        if adminCode == 2:
            self.bot.sendMessage(channel, "Your IDENTIFY with NickServ could not be determined", nick)
        elif adminCode == 1:
            self.bot.sendMessage(channel, "You need to IDENTIFY with NickServ to do that", nick)
        elif adminCode == 0:
            self.bot.sendMessage(channel, "You are not authorized to do that", nick)
        return

    def sendMessage(self, channel, message, nick=''):
        """
        Pass on parameters to the IRC module.

        Notes:
            This should only be used when the bot is running as part of another system.
            Otherwise self.bot.sendMessage() should be called directly

        Args:
            channel (str): channel to send the message in
            message (str): message to send
            nick (str, optional): nick to prefix to the message for highlighting

        Returns:
            None

        Raises:
            None
        """
        self.bot.sendMessage(channel, message, nick)
        return

    def loadModule(self, moduleName):
        """
        Load the module with the give name
        i.e. "admin" would load modules/admin.py

        Args:
            moduleName (str): name of the module (admin would load the admin.py file)

        Returns:
            boolean: success or failure of load

        Raises:
            None
        """
        retLoadedCorrectly = False
        # reload everything to dynamically pick up new stuff
        reload(modules)

        # if the module was already loaded, then we need to reload it
        for cmd in self.loadedModules.keys():
            if self.loadedModules[cmd]['module'] == moduleName:
                modules.reload_modules(moduleName)

        # try to grab the module and get parameters from it
        try:
            # grab the module
            m = getattr(modules, moduleName)

            # save it
            self.loadedModules[m.commandName] = {'module': moduleName, 'admin': m.adminOnly, 'version': m.version, 'help': m.help_msg.strip('\n')}

            # Yay it loaded :)
            retLoadedCorrectly = True

            # log it
            self.log('Loaded module: {0}, {1}, {2}, {3}'.format(moduleName, m.commandName, m.adminOnly, m.version))
        except AttributeError, e:
            self.log('Failed to load module: {0}'.format(moduleName), level='WARNING')
            self.log(e, level='WARNING')

        return retLoadedCorrectly

    def loadModules(self, moduleNames):
        """
        Load the module with the give name
        i.e. "admin" would load modules/admin.py

        Args:
            moduleNames (list): names of the modules to load

        Returns:
            boolean: success or failure of loading all the request modules

        Raises:
            None
        """
        retLoadedCorrectly = True

        for moduleName in moduleNames:
            loadedCorrectly = self.loadModule(moduleName)
            if loadedCorrectly is False:
                retLoadedCorrectly = False

        return retLoadedCorrectly

    def callModule(self, commandName, channel, message, nick):
        """
        Load the module with the give name
        i.e. "admin" would load modules/admin.py

        Args:
            moduleName (str): name of the module (admin would load the admin.py file)

        Returns:
            str: the command used to call the module

        Raises:
            None
        """
        m = getattr(modules, self.loadedModules[commandName]['module'])
        self.log('Calling module: {0}, {1}, {2}'.format(self.loadedModules[commandName]['module'], commandName, self.loadedModules[commandName]['admin']))
        m.execModule(channel, message, nick, self)
        return

    def parseLinePrivmsg(self, channel, message, nick=''):
        """
        Parses the PRIVMSG received from the server

        Args:
            channel (str): channel (or nick if private message chat)
            message (str): message for the bot to handle
            nick (str, optional): nick to highlight in the channel

        Returns:
            None

        Raises:
            None
        """
        self.log("Parsing bot message: ({0} {1}) {2}".format(channel, nick, message), level="DEBUG")
        sourceNick = ''

        # use correct arg for nick
        if nick == '':
            sourceNick = channel
        else:
            sourceNick = nick

        command = message.split()[0]
        messageLen = len(message.split())

        if command in self.loadedModules.keys():
            if self.loadedModules[command]['admin']:
                adminCode = self.isAdminAndIdent(sourceNick)
                if adminCode == 3:
                    self.callModule(command, channel, message, sourceNick)
                else:
                    self.adminCheckFailed(channel, nick, adminCode)
            else:
                self.callModule(command, channel, message, sourceNick)

        elif command == 'quit' and messageLen == 1:
            adminCode = self.isAdminAndIdent(sourceNick)
            if adminCode == 3:
                self.bot.sendMessage(channel, "Bye", nick)
                self.bot.disconnectFromServer()
            else:
                self.adminCheckFailed(channel, nick, adminCode)

        elif command == 'loadModule' and messageLen == 2:
            adminCode = self.isAdminAndIdent(sourceNick)
            if adminCode == 3:
                moduleName = message.split()[1]
                self.bot.sendMessage(channel, "Loading {0}...".format(moduleName), nick)
                didModuleLoad = self.loadModule(moduleName)
                if didModuleLoad is False:
                    self.bot.sendMessage(channel, "Failed to load {0}...".format(moduleName), nick)
            else:
                self.adminCheckFailed(channel, nick, adminCode)

        return

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

        # the server send an error message
        elif len(line.split()) >= 2 and line.split()[0] == "ERROR":
            self.log("{0}".format(line), level="ERROR")

        # invited to a channel
        elif len(line.split()) == 4 and line.split()[1] == "INVITE":
            newChannel = line.split()[3].split(':')[1]
            inviter = line.split()[2]
            self.joinChannel(newChannel)
            self.log("Invited to {0} by {1}".format(newChannel, inviter))

        # kicked from a default channel
        elif len(line.split()) == 5 and line.split()[1] == "KICK" and line.split()[2] in self.channels.keys():
            source = line.split()[0].split(":")[1]
            sourceNick = source.split("!")[0]
            newChannel = line.split()[2]
            self.joinChannel(newChannel)
            self.log("Rejoining default channel {0} since I was kicked by {1}".format(newChannel, sourceNick))

        # the server send a noticed
        elif len(line.split()) >= 2 and line.split()[1] == "NOTICE":
            self.log("{0}".format(line), level="WARNING")

        # first line of the server welcome response
        elif len(line.split()) >= 2 and line.split()[1] == "001":
            server = line.split()[0].split(":")[1]
            self.bot.setActualServer(server)
            self.log("Server is actually {0}".format(server))

        # handle PRIVMSG
        elif len(line.split()) >= 4 and line.split()[1] == "PRIVMSG":
            source = line.split()[0].split(":")[1]
            sourceNick = source.split("!")[0]
            sourceUser = source.split("!")[1].split("@")[0]
            sourceHost = source.split("@")[1]
            destination = line.split()[2]

            # PRIVMSG was sent to a channel
            if destination[0] in self.bot.getChannelPrefixes():
                self.log("PRIVMSG from {0} under {1} on {2} in {3}".format(sourceNick, sourceUser, sourceHost, destination), level="DEBUG")

                # see if the message in the channel was directed at the bot
                if line.split()[3] == ':{0}:'.format(self.bot.getNick()):
                    message = ' '.join(line.split()[4:])
                    self.parseLinePrivmsg(destination, message, sourceNick)

            # PRIVMSG was sent straight to the bot
            else:
                self.log("PRIVMSG from {0} under {1} on {2} at {3}".format(sourceNick, sourceUser, sourceHost, destination), level="DEBUG")
                message = ' '.join(line.split()[3:])

                # the message should be preceded by a : that needs to be removed
                if message[0] == ':':
                    message = message[1:]

                self.parseLinePrivmsg(sourceNick, message)

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

        self.log("{0} has shutdown".format(self.bot.getNick()))
        return

if __name__ == "__main__":
    filename = __file__.split('.')[0]
    help(filename)
