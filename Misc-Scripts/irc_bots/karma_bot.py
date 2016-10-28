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
#| Date: 2016-10-26                                                      |
#+-----------------------------------------------------------------------+
#| Version: 1.0.3                                                        |
#+-----------------------------------------------------------------------+

import socket
import ssl
import json
import threading

server = "localhost"
channel = "#smalltalk"
botnick = "Karmabot"

karma_val = []
karma_num = []

def karmaload():
	global karma_val
	global karma_num
	save_val = open("karma_val.txt")
	save_num = open("karma_num.txt")
	karma_val = json.loads(save_val.read())
	karma_num = json.loads(save_num.read())
	save_val.close()
	save_num.close()

def karmasave():
	threading.Timer(30,karmasave).start()
	global karma_val
	global karma_num
	save_val = file("karma_val.txt", "w")
	save_num = file("karma_num.txt", "w")
	save_val.write(json.dumps(karma_val))
	save_num.write(json.dumps(karma_num))
	save_val.close()
	save_num.close()

karmaload()
karmasave()

irc_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
irc = ssl.wrap_socket(irc_sock)
irc.connect((server, 6667))
irc.send("USER "+ botnick +" "+ botnick +" "+ botnick +" :How much Karma do you have?\n")
irc.send("NICK "+ botnick +"\n")
irc.send("JOIN "+ channel +"\n")


while 1:
	text=irc.recv(2040)
	if text.find('PING') != -1:
		irc.send('PONG ' + text.split() [1] + '\r\n')
	if text.find('++') !=-1 and text.find(channel) !=-1:
		try:
			karma_up = (text.split("++")[0]).split(":")[2].rsplit(None,1)[-1]
		except:
			message = "Who would you like to give Karma to? (e.g. Karmabot++)"
			irc.send('PRIVMSG ' + channel + ' :' + message + '\r\n')
			karma_up = 'null'
		if karma_up in karma_val:
			idx = karma_val.index(karma_up)
			num = karma_num[idx]
			karma_num[idx] = int(num) + 1
		elif karma_up not in karma_val:
			karma_val.append(karma_up)
			karma_num.append(1)
	if text.find('--') !=-1 and text.find(channel) !=-1:
		try:
			karma_down = (text.split("--")[0]).split(":")[2].rsplit(None,1)[-1]
		except:
			message = "Who would you like to take Karma away from? (e.g. Karmabot--)"
			irc.send('PRIVMSG ' + channel + ' :' + message + '\r\n')
			karma_down = 'null'
		if karma_down in karma_val:
			idx = karma_val.index(karma_down)
			num = karma_num[idx]
			karma_num[idx] = int(num) - 1
		elif karma_down not in karma_val:
			karma_val.append(karma_down)
			karma_num.append(-1)
	if text.find('!rank') !=-1 and text.find(channel) !=-1:
		rank = (text.split(':!rank')[1]).strip()
		if rank in karma_val:
			idx = karma_val.index(rank)
			num = karma_num[idx]
			message = (rank + " has " + str(num) + " points of karma!")
			irc.send('PRIVMSG ' + channel + ' :' + message + '\r\n')
		elif rank not in karma_val:
			message = (rank + " doesn't have any karma yet!")
			irc.send('PRIVMSG ' + channel + ' :' + message + '\r\n')
	if text.find('!top') !=-1 and text.find(channel) !=-1:
		top_results = sorted(zip(karma_num,karma_val), reverse=True)[:5]
		irc.send('PRIVMSG ' + channel + ' :' + "## TOP 5 KARMA RECIPIENTS ##" + '\r\n')
		for (x,y) in top_results:
			message = (y + ": " + str(x))
			irc.send('PRIVMSG ' + channel + ' :' + message + '\r\n')
	if text.find('!bottom') !=-1 and text.find(channel) !=-1:
		top_results = sorted(zip(karma_num,karma_val), reverse=False)[:5]
		irc.send('PRIVMSG ' + channel + ' :' + "## BOTTOM 5 KARMA RECIPIENTS ##" + '\r\n')
		for (x,y) in top_results:
			message = (y + ": " + str(x))
			irc.send('PRIVMSG ' + channel + ' :' + message + '\r\n')

