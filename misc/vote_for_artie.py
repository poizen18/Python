#!/usr/local/bin/python

#+-----------------------------------------------------------------------+
#| File Name: vote_for_artie.py                                          |
#+-----------------------------------------------------------------------+   
#| Description: This script votes for Artie on NNFL's website            |
#+-----------------------------------------------------------------------+
#| Usage: Tell the script how many votes Artie should get                |
#+-----------------------------------------------------------------------+
#| Authors: Brian Spaulding                                              |
#+-----------------------------------------------------------------------+
#| Date: 2016-05-07                                                      |
#+-----------------------------------------------------------------------+
#| Version: 1.0.2                                                        |
#+-----------------------------------------------------------------------+

####################################################
#             Import necessary modules             #
####################################################

import re
import sys
import mechanize

####################################################
#     Vote for Artie as many times as specified    #
####################################################

if str.isdigit(sys.argv[1]):
  vote_count = int(sys.argv[1])
else:
  print "Please enter a numeric value"
  exit()

for vote in xrange(vote_count):
  br=mechanize.Browser()
  br.open("http://nnflfootball.com/fun-stuff.html")
  br.form = list(br.forms())[0]
  br.form['qp_v678300'] = ['2']
  vote_button = br.form.find_control(name="qp_b678300", label="Vote")
  vote_button.readonly = False
  br.submit()

print "All done, you voted for Artie %s times" % vote_count
