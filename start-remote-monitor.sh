#!/usr/bin/bash

# Read in the configuration file
source remote-monitor.config

# Assemble the full address of the server
full_server_address=${server_address}::${server_port}

# Attempt to connect
echo Attempting to connect to ${full_server_address}
xinit ${vnc_viewer} ${vnc_flags} ${full_server_address} -- :0 vt${XDG_VTNR} > /dev/null 2>&1
