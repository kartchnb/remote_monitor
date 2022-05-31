#!/usr/bin/python3

import sys

from RemoteMonitor import RemoteMonitor, RemoteMonitorError



def DisplayUsage():
    print('Usage:')
    print(f'{sys.argv[0]} <display number> <horizontal resolution> <vertical resolution> <refresh frequency> <port>')
    print(' Where: <display number> is the virtual display number to use for the remote monitor')
    print('        <horizontal resolution> and <vertical resolution> are the resolution parameters for the remote monitor')
    #print('        <refresh frequency> is the refresh rate (in Hertz) of the remote monitor')
    print('        <port> is the port that VNC should connect to')



# Assemble the required parameters
try:
    display_num = int(sys.argv.pop(1))
    hres = sys.argv.pop(1)
    vres = sys.argv.pop(1)
    port = sys.argv.pop(1)
except IndexError:
    DisplayUsage()
    exit();

# Launch the remote monitor with the given parameters
try:
    print(f'Configuring remote monitor on port {port} using virtual display {display_num} with resolution of {hres}x{vres}')
    RemoteMonitor = RemoteMonitor(display_num, hres, vres, port)
except RemoteMonitorError as e:
    print(f'RemoteMonitor Error: {e.message}')
