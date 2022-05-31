from VirtualDisplay import VirtualDisplay, VirtualDisplayError

virtualDisplay = VirtualDisplay(0, 1920, 1080)
outputName = virtualDisplay.output_name

print(f'outputName={outputName}')