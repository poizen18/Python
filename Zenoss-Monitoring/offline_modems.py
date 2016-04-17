#!/usr/bin/env python

#+-----------------------------------------------------------------------+
#| File Name: offline_modems.py                                          | 
#|                                                                       |
#| Description: Check number of offline modems for each cable node       |
#|                                                                       |
#+-----------------------------------------------------------------------+
#| Authors: wyldbrian and KwithH                                         |
#+-----------------------------------------------------------------------+
#| Date: 2016-03-04                                                      |
#+-----------------------------------------------------------------------+

import paramiko
import subprocess

ubr_ips = ['XXX.XXX.XXX.XXX', 'XXX.XXX.XXX.XXX', 'XXX.XXX.XXX.XXX', 'XXX.XXX.XXX.XXX']
online = []
offline = []
node = []
ubr = []
cableInterface = []

####################################################
#       Gather node information from CMTS(s)       #
####################################################

for ip in ubr_ips:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect( ip, username='EXAMPLEUSER', password='EXAMPLEPASSWORD', look_for_keys=False)
        stdin, stdout, stderr = ssh.exec_command("show cable modem summary")
        for line in stdout:
                if "Cust:" in line and not "No Monitor" in line:
                        online.append(','.join(line.split()).split(",")[1].strip())
                        offline.append(','.join(line.split()).split(",")[5].strip())
                        node.append(line[line.find("{")+1:line.find("}")])
                        ubr.append(line[line.find(":")+1:line.find("[")])
                        cableInterface.append((','.join(line.split())).split(",")[0].strip())
        ssh.close()

####################################################
#     Alert on nodes with high percent offline     #
####################################################
		
for on, off, node, ubr, cableint in zip(online, offline, node, ubr, cableInterface):
        percent = 100 * int(off)/int(on)
        message = "Node %s has %s modems offline (%s%s offline)" % (node, off, percent, '%')
        if "UBR2" in ubr:
                device = 'EXAMPLE-ZENOSS-DEVICE-1'
        elif "UBR3" in ubr:
                device = 'EXAMPLE-ZENOSS-DEVICE-2'
        elif "UBR4" in ubr:
                device = 'EXAMPLE-ZENOSS-DEVICE-3'
        elif "UBR5" in ubr:
                device = 'EXAMPLE-ZENOSS-DEVICE-4'
        if percent >= 50 and int(off) >= 7:
                severity = 'Critical'
        elif percent >= 25 and int(off) >= 5:
                severity = 'Warning'
        elif percent < 25 or int(off) < 5:
                severity = 'Clear'
        subprocess.call(['zensendevent', '-d', device, '-y', cableint, '-p', node, '-s', severity, '-c', '/Cable Plant/Offline Modems', '-k', cableint, message])
