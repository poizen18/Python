#!/usr/local/bin/python

#+-----------------------------------------------------------------------+
#| File Name: turing_bot.py                                              |
#+-----------------------------------------------------------------------+   
#| Description: Turing watches an IRC channel and responds to prompts    |
#+-----------------------------------------------------------------------+
#| Usage: Use ++ or -- to hand out or take away karma (e.g. wyldbrian++) | 
#|        Use !rank to check an items karma rank (e.g. !rank wyldbrian)  |
#|        Use !top to see the top 5 items by karma                       |
#|        Use !bottom to see the bottom 5 items by karma                 |
#!        Use !weather City,State to check weather                       |
#+-----------------------------------------------------------------------+
#| Authors: wyldbrian                                                    |
#+-----------------------------------------------------------------------+
#| Date: 2016-11-08                                                      |
#+-----------------------------------------------------------------------+
#| Version: 1.0                                                          |
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
import logging
import threading

####################################################
#             Set IRC connection values            #
####################################################

server = "localhost"
channel = "#smalltalk"
botnick = "Turing"

####################################################
#              Set logging parameters              #
####################################################

logfile = '/var/log/turing.log'
loglevel = logging.INFO
logformat = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(filename=logfile,format=logformat,level=loglevel)

####################################################
#          Create karma save/load process          #
####################################################

karma_val = []
karma_num = []

def karmaload():
	global karma_val
	global karma_num
	load_val = open("karma_val.json")
	load_num = open("karma_num.json")
	karma_val = json.loads(load_val.read())
	karma_num = json.loads(load_num.read())
	load_val.close()
	load_num.close()

def karmasave():
	threading.Timer(30,karmasave).start()
	global karma_val
	global karma_num
	save_val = file("karma_val.json", "w")
	save_num = file("karma_num.json", "w")
	save_val.write(json.dumps(karma_val))
	save_num.write(json.dumps(karma_num))
	save_val.close()
	save_num.close()

try:
	karmaload()
except:
	logging.critical('Karmaload failed, exiting')
	sys.exit()
else:
	karmasave()

####################################################
#        Create earthquake save/load process       #
####################################################

quake_id = []

def quakeload():
	global quake_id
	load_quakes = open("quake_id.json")
	quake_id = json.loads(load_quakes.read())
	load_quakes.close()

def quakesave():
	threading.Timer(30,quakesave).start()
	global quake_id
	save_quakes = file("quake_id.json", "w")
	save_quakes.write(json.dumps(quake_id))
	save_quakes.close()

try:
	quakeload()
except:
	logging.critical('Quakeload failed, exiting')
	sys.exit()
else:
	quakesave()

####################################################
#          Build karma functions for IRC           #
####################################################

def karmaup():
	try:
		karma_up = (text.split("++")[0]).split(":")[2].rsplit(None,1)[-1]
	except IndexError:
		message = "What would you like to give Karma to? (e.g. Karmabot++)"
		irc.send('PRIVMSG ' + channel + ' :' + message + '\r\n')
		return
	if karma_up in karma_val:
		idx = karma_val.index(karma_up)
		num = karma_num[idx]
		karma_num[idx] = int(num) + 1
		user = (text.split(":")[1]).split("!")[0]
		logmsg = user + " gave karma to " + karma_up + " (++)"
		logging.info(logmsg)
	elif karma_up not in karma_val:
		karma_val.append(karma_up)
		karma_num.append(1)
		user = (text.split(":")[1]).split("!")[0]
		logmsg = user + " gave karma to " + karma_up + " (++)"
		logging.info(logmsg)
		
def karmadown():
	try:
		karma_down = (text.split("--")[0]).split(":")[2].rsplit(None,1)[-1]
	except IndexError:
		message = "What would you like to take Karma away from? (e.g. Karmabot--)"
		irc.send('PRIVMSG ' + channel + ' :' + message + '\r\n')
		return
	if karma_down in karma_val:
		idx = karma_val.index(karma_down)
		num = karma_num[idx]
		karma_num[idx] = int(num) - 1
		user = (text.split(":")[1]).split("!")[0]
		logmsg = user + " took karma away from " + karma_down + " (--)"
		logging.info(logmsg)
	elif karma_down not in karma_val:
		karma_val.append(karma_down)
		karma_num.append(-1)
		user = (text.split(":")[1]).split("!")[0]
		logmsg = user + " took karma away from " + karma_down + " (--)"
		logging.info(logmsg)
		
def karmarank():
	try:
		rank = (text.split(':!rank')[1]).strip()
	except IndexError:
		message = "What would you like to check the rank of? (e.g. !rank Karmabot)"
		irc.send('PRIVMSG ' + channel + ' :' + message + '\r\n')
		return
	if rank in karma_val:
		idx = karma_val.index(rank)
		num = karma_num[idx]
		message = (rank + " has " + str(num) + " points of karma!")
		irc.send('PRIVMSG ' + channel + ' :' + message + '\r\n')
	elif rank not in karma_val:
		message = (rank + " doesn't have any karma yet!")
		irc.send('PRIVMSG ' + channel + ' :' + message + '\r\n')
		
def topkarma():
	top_results = sorted(zip(karma_num,karma_val), reverse=True)[:5]
	irc.send('PRIVMSG ' + channel + ' :' + "## TOP 5 KARMA RECIPIENTS ##" + '\r\n')
	for (x,y) in top_results:
		message = (y + ": " + str(x))
		irc.send('PRIVMSG ' + channel + ' :' + message + '\r\n')
		
def bottomkarma():
	top_results = sorted(zip(karma_num,karma_val), reverse=False)[:5]
	irc.send('PRIVMSG ' + channel + ' :' + "## BOTTOM 5 KARMA RECIPIENTS ##" + '\r\n')
	for (x,y) in top_results:
		message = (y + ": " + str(x))
		irc.send('PRIVMSG ' + channel + ' :' + message + '\r\n')		

####################################################
#          Build weather function for IRC          #
####################################################

def weathercheck():
	try:
		city = (text.split("!weather")[1]).split(",")[0].lstrip().replace(" ","_")
		state = (text.split("!weather")[1]).split(",")[1].strip().replace(" ","_")
	except IndexError:
		message = "What city's weather would you like to check? (e.g. !weather Bend,OR)"
		irc.send('PRIVMSG ' + channel + ' :' + message + '\r\n')
		return
	weather_call = urllib2.urlopen('http://api.wunderground.com/api/0c6e61e8fe3d5798/geolookup/conditions/q/%s/%s.json' %(state,city), timeout = 1)
	weather_output = weather_call.read()
	weather_call.close()
	weather_dict = json.loads(weather_output)
	try:
		temp = weather_dict['current_observation']['temperature_string']
		location = weather_dict['location']['city']
		condition = weather_dict['current_observation']['weather']
	except KeyError:
		if "keynotfound" in weather_output:
			message = ("Weather API rate limit reached, please try again in a few seconds.")
			irc.send('PRIVMSG ' + channel + ' :' + message + '\r\n')
			logging.warning(message)
			return
		elif "querynotfound" in weather_output:
			message = ("No weather results found for %s,%s" %(city,state))
			irc.send('PRIVMSG ' + channel + ' :' + message + '\r\n')
			logging.warning(message)
			return
		else:
			return
	message = "The weather in %s is currently showing %s with a temperature of %s" %(location,condition,temp) 
	irc.send('PRIVMSG ' + channel + ' :' + message + '\r\n')

####################################################
#       Build function for earthquake checks       #
####################################################	

def quakecheck():
	threading.Timer(900,quakecheck).start()
	try:
		quake_call = urllib2.urlopen('http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_hour.geojson', timeout = 1)
	except:
		message = "Caught exception trying to connect to usgs api"
		logging.CRITICAL(message)
		return
	quake_output = quake_call.read()
	quake_call.close
	quake_dict = json.loads(quake_output)
	global quake_id
	for quake in quake_dict['features']:
		if quake['id'] not in quake_id:
			quake_id.append(quake['id'])
			mag = quake['properties']['mag']
			location = quake['properties']['place']
			message = "%s magnitude earthquake detected %s" %(mag,location)
			try:
				irc.send('PRIVMSG ' + channel + ' :' + message + '\r\n')
			except:
				message = "Caught exception trying to post quake info to IRC"
				logging.critical(message)
				return
			logging.warning(message)
			
####################################################
#              Build IRC help function             #
####################################################

def help():
	irc.send('PRIVMSG ' + channel + ' :' + "     ##############################TURING USAGE##############################" + '\r\n')
	irc.send('PRIVMSG ' + channel + ' :' + "     !weather = check weather for a specific location (e.g. !weather Bend,OR)" + '\r\n')
	irc.send('PRIVMSG ' + channel + ' :' + "     ++ or -- = give or take karma from whatever you want (e.g. Turing++)" + '\r\n')
	irc.send('PRIVMSG ' + channel + ' :' + "     !rank = show the rank of a particular thing (e.g. !rank Turing--)" + '\r\n')
	irc.send('PRIVMSG ' + channel + ' :' + "     !top or !bottom = show the top or bottom 5 items by Karma" + '\r\n')

####################################################
#            Build IRC connect function            #
####################################################

def connect():
	global irc_sock
	global irc
	irc_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	irc = ssl.wrap_socket(irc_sock)
	irc.connect((server, 6667))
	irc.send("USER "+ botnick +" "+ botnick +" "+ botnick +" :Machines take me by surprise with great frequency.\n")
	irc.send("NICK "+ botnick +"\n")
	irc.send("JOIN "+ channel +"\n")

####################################################
# Watch IRC chat for key values and run functions  #
####################################################	

connect()

quakecheck()

while 1:
	text=irc.recv(1024)
	if text.find('PING') != -1:
		irc.send('PONG ' + text.split() [1] + '\r\n')
	elif text.find('++') !=-1 and text.find(channel) !=-1:
		karmaup()
	elif text.find('--') !=-1 and text.find(channel) !=-1:
		karmadown()
	elif text.find('!rank') !=-1 and text.find(channel) !=-1:
		karmarank()
	elif text.find('!top') !=-1 and text.find(channel) !=-1:
		topkarma()
	elif text.find('!bottom') !=-1 and text.find(channel) !=-1:
		bottomkarma()
	elif text.find('!weather') !=-1 and text.find(channel) !=-1:
		weathercheck()
	elif text.find('!help') !=-1 and text.find(channel) !=-1:
		time.sleep(.5)
		help()
	elif len(text) == 0:
		while 1:
			try:
				time.sleep(300)
				connect()
			except:
				continue
			break
