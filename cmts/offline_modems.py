#!/usr/bin/env python

#+-----------------------------------------------------------------------+
#| File Name: offline_modems_threaded.py                                 |
#|                                                                       |
#| Description: Check number of offline modems for each cable node       |
#|                                                                       |
#+-----------------------------------------------------------------------+
#| Authors: wyldbrian and KwithH                                         |
#+-----------------------------------------------------------------------+
#| Date: 2016-03-10                                                      |
#+-----------------------------------------------------------------------+

import paramiko
import subprocess
from threading import Thread

ubr_ips = 	['XXX.XXX.XXX.XXX', 'XXX.XXX.XXX.XXX', 'XXX.XXX.XXX.XXX', 'XXX.XXX.XXX.XXX']
ubr_names =	['ZENOSS.DEVICE.1', 'ZENOSS.DEVICE.2', 'ZENOSS.DEVICE.3', 'ZENOSS.DEVICE.4']

####################################################
#       Gather node information from CMTS(s)       #
####################################################

def offlinealert(ip, name):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect( ip, username='YOURUSERNAME', password='YOURPASSWORD', look_for_keys=False)
        stdin, stdout, stderr = ssh.exec_command("show cable modem summary")
        for line in stdout:
                if "Cust:" in line and not "No Monitor" in line:
                        on = (','.join(line.split()).split(",")[1].strip())
                        off = (','.join(line.split()).split(",")[5].strip())
                        node = (line[line.find("{")+1:line.find("}")])
                        cableint = ((','.join(line.split())).split(",")[0].strip())
				percent = 100 * int(offline)/int(online)
				message = "Node %s has %s modems offline (%s%s offline)" % (node, off, percent, '%')
				if percent >= 50 and int(off) >= 7:
					severity = 'Critical'
				elif percent >= 25 and int(off) >= 5:
					severity = 'Warning'
				elif percent < 25 or int(off) < 5:
					severity = 'Clear'
				subprocess.call(['zensendevent', '-d', name, '-y', cableint, '-p', node, '-s', severity, '-c', '/Cable Plant/Offline Modems', '-k', cableint, message])
        ssh.close()

####################################################
#  Thread each SSH connection and generate events  #
####################################################


t1 = Thread(target=offlinealert, args=(ubr_ips[0],ubr_names[0],))
t2 = Thread(target=offlinealert, args=(ubr_ips[1],ubr_names[1],))
t3 = Thread(target=offlinealert, args=(ubr_ips[2],ubr_names[2],))
t4 = Thread(target=offlinealert, args=(ubr_ips[3],ubr_names[3],))
threads.extend([t1, t2, t3, t4])

for t in threads:
        t.start()

for t in threads:
        t.join()

