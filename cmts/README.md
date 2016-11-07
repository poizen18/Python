# CMTS Monitoring Scripts

## Offline Modems (offline_modems.py)

## How it works:
This script will connect to multiple UBRs (Cisco UBR10Ks in this case) and pull cable modem stats for alerting purposes. 
- The paramiko python module is used to handle SSH
- The ouput of "show cable modem summary" is parsed out into total modems, offline modems, node, and cable interface
- The percentage of offline modems based on the total is calculated and alerted on based on percentage
- If percentage thresholds are broken, and alarm is generated and sent to Zenoss

## UBR Arp Check (ubr10k_arp_check.py)

## How it works:
This script will connect to multiple UBRs (Cisco UBR10Ks in this case) and pull the arp table for review.
- The paramiko module is used to handle SSH
- The output of "show arp" is appended to an array called macs
- The contents of macs is reviewed for multiple occurrences of the same mac (excluding gateways and private address space)
- If the number of occurences breaks a specific threshold, and alarm containing the offending mac address is sent to Zenoss
- Exiting alarms are pulled and dumped into an array called alarms for review prior to creating new alarms 
