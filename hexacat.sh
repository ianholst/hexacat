#!/bin/bash
# Start wifi AP
# hostapd -B /etc/hostapd.conf
sleep 10
# update time
# sntp -s time.nist.gov
# check for git update
cd /root/hexacat
git pull
# Start python script
python hexacat.py
