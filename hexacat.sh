#!/bin/bash
# check for git update
git pull
chmod +x /root/hexacat/hexacat.sh
python /root/hexacat/hexacat.py
