#!/bin/bash
# Start wifi AP
hostapd -B /etc/hostapd.conf
# update time
sntp -s time.nist.gov
# check for git update
git pull
# Start python script
python /root/hexacat/hexacat.py
