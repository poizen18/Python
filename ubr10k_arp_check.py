#!/usr/bin/env python

#+-----------------------------------------------------------------------+
#| File Name: ubr10k_arp_check.py                                        |
#+-----------------------------------------------------------------------+   
#| Description: This script checks UBR10K arp tables for abusive devices |
#+-----------------------------------------------------------------------+
#| Usage: pass UBR10K IP addresses to the script for processing          |
#+-----------------------------------------------------------------------+
#| Authors: wyldbrian                                                    |
#+-----------------------------------------------------------------------+
#| Date: 2016-04-15                                                      |
#+-----------------------------------------------------------------------+
#| Version: 1.1.0                                                        |
#+-----------------------------------------------------------------------+

####################################################
#             Import necessary modules             #
####################################################

import paramiko
import subprocess
import MySQLdb
import sys
import os
import socket
from threading import Thread
from collections import Counter

####################################################
#            Enable or disable debugging           #
####################################################

DEBUG = False

####################################################
#         Pull active alarms from MySQL DB         #
####################################################

db = MySQLdb.connect("localhost","YOURUSER","YOURPASSWORD","zenoss_zep")
cursor = db.cursor()
cursor.execute("SELECT event_key FROM v_event_summary WHERE event_class = '/Cable Plant/IP Abuse' AND status_id in ('0','1')")
rows = cursor.fetchall()
db.close()

alarms = []
for row in rows:
        alarms.append(row[0])

if DEBUG = True
        for alarm in alarms:
                print "Mac address %s has an active alarm" % alarm

####################################################
#       Confirm that each device is a UBR10K       #
####################################################

ubr_ips = []
devnull = open(os.devnull, 'w')
for ip in sys.argv:
        try:
                check_model = str(subprocess.check_output(['snmpget', '-v2c', '-ccaution', ip, 'sysDescr.0'], stderr=devnull))
                if "UBR10K" in check_model:
                        ubr_ips.append(ip)
        except:
                print "%s is not a valid UBR10K IP address or hostname" % ip
                pass

if DEBUG = True
        for ip in ubr_ips:
                name = str(subprocess.check_output(['snmpget', '-v2c', '-ccaution', ip, 'sysName.0'])).rsplit(None, 1)[-1]
                print "Device %s(%s) is ready for processing" % (name, ip)

####################################################
#       Build function to gather arp tables        #
####################################################

def ipabusealert(ip):
        macs = []
        name = str(subprocess.check_output(['snmpget', '-v2c', '-ccaution', ip, 'sysName.0'])).rsplit(None, 1)[-1]
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
                ssh.connect( ip, username='YOURUSER', password='YOURPASSWORD', look_for_keys=False, timeout=2)
        except:
                message = "Unable to SSH into %s to gather arp table" % name
                subprocess.call(['zensendevent', '-d', name, '-y', 'ssh_error', '-p', 'SSH Error', '-s', 'Info', '-c', '/Cable Plant/', '-k', 'ssh_error', message])
                sys.exit(0)
        stdin, stdout, stderr = ssh.exec_command("show arp")
        for line in stdout:
                if "Bundle" in line and not " 10." in line and not ".1 " in line:
                        try:
                                macs.append(line.split()[3].strip())
                        except IndexError:
                                pass
        ssh.close()
        counter_mac = Counter(macs)
        for mac in counter_mac:
                if counter_mac[mac] >= 10:
                        message = "Customer mac address %s has %s entries in the arp table" % (mac, counter_mac[mac])
                        subprocess.call(['zensendevent', '-d', name, '-y', mac, '-p', mac, '-s', 'Info', '-c', '/Cable Plant/IP Abuse', '-k', mac, message])
                elif mac in alarms:
                        message = "Customer mac address %s has %s entries in the arp table" % (mac, counter_mac[mac])
                        subprocess.call(['zensendevent', '-d', name, '-y', mac, '-p', mac, '-s', 'Clear', '-c', '/Cable Plant/IP Abuse', '-k', mac, message])

####################################################
#     Call threaded function for each device       #
####################################################

for ip in ubr_ips:
        t = Thread(target=ipabusealert, args=(ip,))
        t.start()
        t.join()
