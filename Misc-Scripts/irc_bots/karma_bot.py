#!/usr/local/bin/python

#+-----------------------------------------------------------------------+
#| File Name: karma_bot.py                                               |
#+-----------------------------------------------------------------------+   
#| Description: Give positive or negative karma to whatever you want     |
#+-----------------------------------------------------------------------+
#| Usage: Use "++" or "--" to hand out karma in irc (e.g. wyldbrian++)   |
#+-----------------------------------------------------------------------+
#| Authors: Brian Spaulding                                              |
#+-----------------------------------------------------------------------+
#| Date: 2016-10-31                                                      |
#+-----------------------------------------------------------------------+
#| Version: 1.1.2                                                        |
#+-----------------------------------------------------------------------+

####################################################
#             Import necessary modules             #
####################################################

import ssl
import sys
import json
import time
import socket
import threading

####################################################
#             Set IRC connection values            #
####################################################

server = "localhost"
channel = "#smalltalk"
botnick = "Karmabot"

####################################################
#  Initialize arrays and create load/save process  #
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
	print "Karmaload failed, exiting"
	sys.exit()
else:
	karmasave()

####################################################
#            Build IRC connect function            #
####################################################

def connect():
	global irc_sock
	global irc
	irc_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	irc = ssl.wrap_socket(irc_sock)
	irc.connect((server, 6667))
	irc.send("USER "+ botnick +" "+ botnick +" "+ botnick +" :How much Karma do you have?\n")
	irc.send("NICK "+ botnick +"\n")
	irc.send("JOIN "+ channel +"\n")

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
	elif karma_up not in karma_val:
		karma_val.append(karma_up)
		karma_num.append(1)
		
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
	elif karma_down not in karma_val:
		karma_val.append(karma_down)
		karma_num.append(-1)
		
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

def karmahelp():
	irc.send('PRIVMSG ' + channel + ' :' + "     ############################KARMABOT USAGE############################" + '\r\n')
	irc.send('PRIVMSG ' + channel + ' :' + "     ++ or -- = give or take karma from whatever you want (e.g. Karmabot++)" + '\r\n')
	irc.send('PRIVMSG ' + channel + ' :' + "     !rank = show the rank of a particular thing (e.g. !rank Karmabot)" + '\r\n')
	irc.send('PRIVMSG ' + channel + ' :' + "     !top or !bottom = show the top or bottom 5 items by Karma" + '\r\n')	

####################################################
# Watch IRC chat for key values and run functions  #
####################################################	

connect()

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
	elif text.find('!help') !=-1 and text.find(channel) !=-1:
		time.sleep(.5)
		karmahelp()
	elif len(text) == 0:
		while 1:
			try:
				time.sleep(300)
				connect()
			except:
				continue
			break
