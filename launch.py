#!/usr/bin/python3

import sys

from RemoteMonitor import RemoteMonitor, RemoteMonitorError

def DisplayUsage():
    print('Usage:')
    print(f'{sys.argv[0]} <display number> <horizontal resolution> <vertical resolution> <refresh frequency> [cache value]')
    print(' Where: <display number> is the virtual display number to use for the remote monitor')
    print('        <horizontal resolution> and <vertical resolution> are the resolution parameters for the remote monitor')
    print('        <refresh frequency> is the refresh rate (in Hertz) of the remote monitor')
    print('        [cache value] is the optional VNC caching value to use')

try:
    display_num = int(sys.argv[1])
    hres = sys.argv[2]
    vres = sys.argv[3]
    freq = sys.argv[4]
except IndexError:
    DisplayUsage()
    exit();

try:
    ncache = int(sys.argv[5])
except IndexError:
    ncache = 0

try:
    print(f'Configuring remote monitor using virtual display {display_num} with resolution of {hres}x{vres} at {freq} Hz')
    RemoteMonitor = RemoteMonitor(display_num, hres, vres, freq)
except RemoteMonitorError as e:
    print(f'RemoteMonitor Error: {e.message}')
