#!/usr/local/bin/python

import commands
import socket
import sys
import ssl

server = "irc.wyldbrian.com"   
channel = "#smalltalk"
botnick = "wyldbot"

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
   if text.find(':!hi') !=-1:
      t = text.split(':!hi')
      to = t[1].strip()
      irc.send('PRIVMSG '+channel+' :Hello'+str(to)+'! \r\n')
   if text.find(':!plex') !=-1:
      t = text.split(':!plex')
      to = t[1].strip()
      output = commands.getoutput('ps -A')
      if 'Plex' in output:
         irc.send('PRIVMSG '+channel+' :Plex server is running'+str(to)+'! \r\n')
      else:
	 irc.send('PRIVMSG '+channel+' :Plex server is not running'+str(to)+'! \r\n')
