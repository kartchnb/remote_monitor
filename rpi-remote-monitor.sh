#!/usr/bin/bash

title='RPI Remote Monitor'
hres=1920
vres=1080
port=5901

# Change the terminal title
echo -ne "\033]0;${title} (port ${port})\007"
/usr/bin/python3 /home/brad/MEGA/Code/remote_monitor/init-remote-monitor.py $hres $vres $port
