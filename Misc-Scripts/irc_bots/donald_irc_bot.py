#!/usr/local/bin/python

import socket
import random
import ssl
import sys
import time

server = "localhost"
channel = "#smalltalk"
botnick = "Donald"

irc_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
irc = ssl.wrap_socket(irc_sock)
irc.connect((server, 6667))
irc.send("USER "+ botnick +" "+ botnick +" "+ botnick +" :Annoying little bot\n")
irc.send("NICK "+ botnick +"\n")
irc.send("JOIN "+ channel +"\n")

while 1:
   text=irc.recv(2040)
   print text
   if text.find('PING') != -1:
      irc.send('PONG ' + text.split() [1] + '\r\n')
   if text.lower().find('trump') !=-1:
      quote = random.choice(list(open('donald_quotes.txt')))
      time.sleep(2)
      irc.send('PRIVMSG ' + channel + ' :' + quote + '\r\n')
