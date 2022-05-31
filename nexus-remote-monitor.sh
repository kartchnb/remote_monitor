#!/usr/bin/bash

title='Nexus 7 Remote Monitor'
display_num=2
hres=960
vres=600

# Calculate the port that will be used (5900 + display number)
let port=5900+display_num

# Change the terminal title
echo -ne "\033]0;${title} (port ${port})\007"
/usr/bin/python3 /home/brad/MEGA/Code/remote_monitor/launch.py $display_num $hres $vres $port
