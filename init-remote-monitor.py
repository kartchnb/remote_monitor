#!/usr/bin/python3

import sys

from RemoteMonitor import RemoteMonitor, RemoteMonitorError



def DisplayUsage():
    print('Usage:')
    print(f'{sys.argv[0]} <horizontal resolution> <vertical resolution> [port]')
    print(' Where: <horizontal resolution> and <vertical resolution> are the resolution parameters for the remote monitor')
    print('        [port] is the port that VNC should use for this remote-monitor (defaults to 5900)')



# Assemble the required parameters
try:
    hres = sys.argv.pop(1)
    vres = sys.argv.pop(1)
except IndexError:
    DisplayUsage()
    exit();

# Assemble the optional parameters
try:
    port = sys.argv.pop(1)
except IndexError:
    port = 5900

# Launch the remote monitor with the given parameters
try:
    print(f'Configuring a remote monitor with resolution of {hres}x{vres} using port {port}')
    RemoteMonitor = RemoteMonitor(hres, vres, port)
except RemoteMonitorError as e:
    print(f'RemoteMonitor Error: {e.message}')