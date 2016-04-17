#!/usr/local/bin/python

#+-----------------------------------------------------------------------+
#| File Name: home_access.py                                             |
#|                                                                       |
#| Description: Check if source is in firewall and add it if it's not    |
#|                                                                       |
#+-----------------------------------------------------------------------+
#| Authors: wyldbrian                                                    |
#+-----------------------------------------------------------------------+
#| Date: 2016-03-23                                                      |
#+-----------------------------------------------------------------------+

import socket
import subprocess
import os

ip = socket.gethostbyname('irc.wyldbrian.com')
firewall = subprocess.check_output(['firewall-cmd', '--zone=trusted', '--list-sources'])
devnull = open(os.devnull, 'w')

if ip not in firewall:
        subprocess.call(['firewall-cmd', '--reload'], stdout=devnull, stderr=devnull)
        subprocess.call(['firewall-cmd', '--zone=trusted', '--add-source=' + ip], stdout=devnull, stderr=devnull)
elif ip in firewall:
        exit
