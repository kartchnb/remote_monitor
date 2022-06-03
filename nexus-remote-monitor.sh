#!/usr/bin/bash

title='Nexus 7 Remote Monitor'
hres=960
vres=600
port=5902

# Change the terminal title
echo -ne "\033]0;${title} (port ${port})\007"
/usr/bin/python3 /home/brad/MEGA/Code/remote_monitor/init-remote-monitor.py $hres $vres $port

