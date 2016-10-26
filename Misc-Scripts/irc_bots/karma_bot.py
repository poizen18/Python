#!/usr/local/bin/python

import socket
import ssl
import sys
import time
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
	if text.find('++') !=-1:
		karma_up = (text.split("++")[0]).split(":")[2]
		if karma_up in karma_val:
			idx = karma_val.index(karma_up)
			num = karma_num[idx]
			karma_num[idx] = int(num) + 1
		elif karma_up not in karma_val:
			karma_val.append(karma_up)
			karma_num.append(1)
	if text.find('--') !=-1:
		karma_down = (text.split("--")[0]).split(":")[2]
		if karma_down in karma_val:
			idx = karma_val.index(karma_down)
			num = karma_num[idx]
			karma_num[idx] = int(num) - 1
		elif karma_down not in karma_val:
			karma_val.append(karma_down)
			karma_num.append(-1)
	if text.find('!rank') !=-1:
		rank = (text.split(':!rank')[1]).strip()
		if rank in karma_val:
			idx = karma_val.index(rank)
			num = karma_num[idx]
			message = (rank + " has " + str(num) + " points of karma!")
			irc.send('PRIVMSG ' + channel + ' :' + message + '\r\n')
		elif rank not in karma_val:
			message = (rank + " doesn't have any karma yet!")
			irc.send('PRIVMSG ' + channel + ' :' + message + '\r\n')
