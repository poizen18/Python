#!/usr/local/bin/python

#+-----------------------------------------------------------------------+
#| File Name: media_backup.py                                            |
#|                                                                       |
#| Description: Use rsync to backup media                                |
#|                                                                       |
#+-----------------------------------------------------------------------+
#| Authors: wyldbrian                                                    |
#+-----------------------------------------------------------------------+
#| Date: 2016-03-23                                                      |
#+-----------------------------------------------------------------------+

import syslog
import subprocess
import os

check = str(os.path.ismount('/mnt/backup'))
devnull = open(os.devnull, 'w')

if check is 'True':
	subprocess.call(['rsync', '-azq', '/media/', '/home/', '/mnt/backup/Plex-Media/'], stdout=devnull, stderr=devnull)
	syslog.syslog('Rsync backup completed')
elif check is 'False':
	syslog.syslog('Rsync backup failed, NAS not mounted')
