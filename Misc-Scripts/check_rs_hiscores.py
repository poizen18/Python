#!/usr/local/bin/python

#+-----------------------------------------------------------------------+
#| File Name: check_rs_hiscores.py                                       |
#+-----------------------------------------------------------------------+   
#| Description: This script checks your hiscores on runescape's site     |
#+-----------------------------------------------------------------------+
#| Usage: Tell the script which player you would like to lookup          |
#+-----------------------------------------------------------------------+
#| Authors: Brian Spaulding                                              |
#+-----------------------------------------------------------------------+
#| Date: 2016-05-20                                                      |
#+-----------------------------------------------------------------------+
#| Version: 1.0.0                                                        |
#+-----------------------------------------------------------------------+

####################################################
#             Import necessary modules             #
####################################################

import sys
import urllib2

player = sys.argv[1]

url = "http://us.battle.net/api/wow/character/thrall/wyldbrian"

response = urllib2.urlopen(url)
html = response.read()
