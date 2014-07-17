#!/usr/bin/env python
# =============================================================================
# file = weather.py
# description = gbot module
# author = GR <https://github.com/shortdudey123>
# create_date = 2014-07-12
# mod_date = 2014-07-12
# version = 0.1
# usage = loaded by gbot
# notes =
# python_ver = 2.7.6
# =============================================================================

import urllib
import json
import re

adminOnly = False
commandName = 'weather'
version = 0.1
help = """
Gets the weather for the given US airport code
Usage: {0} <IATA airpot code>
Admin Only: {1}
Version: {2}
Note: information on IATA codes can be found at the following links
    http://www.iata.org/publications/Pages/code-search.aspx
    http://en.wikipedia.org/wiki/International_Air_Transport_Association_airport_code
""".format(commandName, adminOnly, version)

def execModule(channel, message, nick, botSelf):
    retCommands = []
    re_iata = "^[A-Z][A-Z][A-Z]$"
    re_zipCode = "^[0-9][0-9][0-9][0-9][0-9]$"

    if len(message.split()) == 1:
        pass
    elif len(message.split()) == 2:
        location = message.split()[1]
        weatherInfo = []
        botSelf.log("Getting weather info for {0}".format(location.upper()))

        if len(location) == 3 and re.match(re_iata, location.upper()):
            requestData = urllib.urlopen('http://services.faa.gov/airport/status/{0}?format=json'.format(location))
            try:
                data = json.load(requestData)
                weatherInfo.append('{0} ({1}) in {2}, {3}'.format(data['name'], data['IATA'], data['city'], data['state']))
                weatherInfo.append('Temperature: {0}'.format(data['weather']['temp']))
                weatherInfo.append('Visibility: {0}m'.format(data['weather']['visibility']))
                weatherInfo.append('Sky: {0}'.format(data['weather']['weather']))
                weatherInfo.append('Wind: {0}'.format(data['weather']['wind']))
                weatherInfo.append('Last updated: {0}'.format(data['weather']['meta']['updated']))
                botSelf.log("Got weather info for IATA {0}".format(location.upper()))
            except ValueError, e:
                botSelf.bot.sendMessage(channel, 'Please use a valid IATA airport code (http://www.iata.org/publications/Pages/code-search.aspx or Wikipidia)')
                botSelf.log("Failed to get weather info for IATA {0}".format(location.upper()))

        elif len(location) == 5 and re.match(re_zipCode, location):
            botSelf.bot.sendMessage(channel, 'Zip codes are not supported yet.  Sorry :(')            

        if weatherInfo != []:
            for line in weatherInfo:
                botSelf.bot.sendMessage(channel, line)

    return retCommands

if __name__ == "__main__":
    filename = __file__.split('.')[0]
    help(filename)