#!/usr/bin/python3

from VirtualDisplay import VirtualDisplay, VirtualDisplayError

try:
    virtualDisplay = VirtualDisplay(1920, 1080)
    outputName = virtualDisplay.output_name
    print(f'outputName={outputName}')

except VirtualDisplayError as e:
    print(f'ERROR: {e.message}')
