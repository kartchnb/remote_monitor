#!/usr/bin/bash

title='RPI Remote Monitor'
display_num=1
hres=1920
vres=1080

# Calculate the port that will be used (5900 + display number)
let port=5900+display_num

# Change the terminal title
echo -ne "\033]0;${title} (port ${port})\007"
/usr/bin/python3 /home/brad/MEGA/Code/remote_monitor/launch.py $display_num $hres $vres $port
