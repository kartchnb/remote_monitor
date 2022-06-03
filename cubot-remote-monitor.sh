#!/usr/bin/bash

title='Cubot X19 Remote Monitor'
hres=720
vres=360
port=5903

# Change the terminal title
echo -ne "\033]0;${title} (port ${port})\007"
/usr/bin/python3 /home/brad/MEGA/Code/remote_monitor/init-remote-monitor.py $hres $vres $port
