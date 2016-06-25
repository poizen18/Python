#!/usr/local/bin/python

import socket
import random
import sys
import time

server = "irc.wyldbrian.com"
channel = "#smalltalk"
botnick = "Donald"

irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
irc.connect((server, 6667))
irc.send("USER "+ botnick +" "+ botnick +" "+ botnick +" :Annoying little bot\n")
irc.send("NICK "+ botnick +"\n")
irc.send("JOIN "+ channel +"\n")

trumps = ['trump','Trump', '!trump', '!Trump']

while 1:
   text=irc.recv(2040)
   print text
   if text.find('PING') != -1:
      irc.send('PONG ' + text.split() [1] + '\r\n')
   for trump in trumps:
      if text.find(trump) !=-1:
         quote = random.choice(list(open('donald_quotes.txt')))
         time.sleep(2)
         irc.send('PRIVMSG ' + channel + ' :' + quote + '\r\n')
