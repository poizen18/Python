#!/usr/local/bin/python

#+-----------------------------------------------------------------------+
#| File Name: weather_bot.py                                             |
#+-----------------------------------------------------------------------+
#| Description: Check weather for a specific city                        |
#+-----------------------------------------------------------------------+
#| Usage: User !weather City,State to display weather in IRC             |
#+-----------------------------------------------------------------------+
#| Authors: Brian Spaulding                                              |
#+-----------------------------------------------------------------------+
#| Date: 2016-11-7                                                       |
#+-----------------------------------------------------------------------+
#| Version: 1.1                                                          |
#+-----------------------------------------------------------------------+

####################################################
#             Import necessary modules             #
####################################################

import ssl
import sys
import json
import time
import socket
import urllib2

####################################################
#             Set IRC connection values            #
####################################################

server = "localhost"
channel = "#smalltalk"
botnick = "weatherbot"

####################################################
#            Build IRC connect function            #
####################################################

def connect():
        global irc_sock
        global irc
        irc_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        irc = ssl.wrap_socket(irc_sock)
        irc.connect((server, 6667))
        irc.send("USER "+ botnick +" "+ botnick +" "+ botnick +" :Check the weather for any city.\n")
        irc.send("NICK "+ botnick +"\n")
        irc.send("JOIN "+ channel +"\n")

		
####################################################
#          Build weather function for IRC          #
####################################################

def weather():
        try:
		city = (text.split("!weather")[1]).split(",")[0].lstrip().replace(" ","_")
		state = (text.split("!weather")[1]).split(",")[1].strip().replace(" ","_")
        except IndexError:
                message = "What city's weather would you like to check? (e.g. !weather Bend,OR)"
                irc.send('PRIVMSG ' + channel + ' :' + message + '\r\n')
                return
	api = urllib2.urlopen('http://api.wunderground.com/api/0c6e61e8fe3d5798/geolookup/conditions/q/%s/%s.json' % (state,city))
	json_string = api.read()
	parsed_json = json.loads(json_string)
	try:
		temp = parsed_json['current_observation']['temperature_string']
		location = parsed_json['location']['city']
		condition = parsed_json['current_observation']['weather']
	except:
		message = ("What city's weather would you like to check? (e.g. !weather Bend,OR)")
		irc.send('PRIVMSG ' + channel + ' :' + message + '\r\n')
		return
	message = "The weather in %s is currently showing %s with a temperature of %s" %(location,condition,temp) 
	irc.send('PRIVMSG ' + channel + ' :' + message + '\r\n')
	api.close()


####################################################
# Watch IRC chat for key values and run functions  #
####################################################

connect()

while 1:
        text=irc.recv(1024)
        if text.find('PING') != -1:
                irc.send('PONG ' + text.split() [1] + '\r\n')
        elif text.find('!weather') !=-1 and text.find(channel) !=-1:
                weather()
        elif len(text) == 0:
                while 1:
                        try:
                                time.sleep(300)
                                connect()
                        except:
                                continue
                        break
