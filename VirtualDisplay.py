import re
import signal

from RunCommand import RunCommand


# TODO: See if we an remove all xrandr system calls and do this organically


class VirtualDisplay:

    # The minimum and maximum virtual display numbers to support
    _minVirtualDisplayNum = 1
    _maxVirtualDisplayNum = 9

    # Standard frequency for all remote monitors
    _frequency = 5
    
    def __init__(self, hres, vres):
        self.output_name = ''
        
        # Determine the mode name 
        self.mode_name = f'RM_{hres}x{vres}'

        # Iterate over each possible virtual display name
        for display_num in range(self._minVirtualDisplayNum, self._maxVirtualDisplayNum + 1):
            # If this display name is available, use it
            result = RunCommand('xrandr')
            search_string = f'VIRTUAL{display_num} disconnected'
            print(f'Searching for "{search_string}"')
            match = re.search(search_string, result)
            if (match):
                self.output_name = f'VIRTUAL{display_num}'
                break

        if self.output_name == '':
            raise VirtualDisplayError('No available virtual displays were found')

        # Determine the parameters for the new display
        mode_params = self._GenerateXrandrParams(hres, vres, self._frequency)

        # Create the new display mode
        RunCommand(f'xrandr --newmode {self.mode_name} {mode_params}')

        # Add the display mode for the requested output
        RunCommand(f'xrandr --addmode {self.output_name} {self.mode_name}')

        # Enable the requested output using the new display mode
        RunCommand(f'xrandr --output {self.output_name} --mode {self.mode_name}')

        # Add a handler for CTRL-C
        signal.signal(signal.SIGINT, self._CtrlCHandler)



    def __del__(self):
        self.Close()



    # Close the virtual display
    def Close(self):
        # Delete the virtual display
        if self.output_name != '':
            RunCommand(f'xrandr --output {self.output_name} --off')
            RunCommand(f'xrandr --delmode {self.output_name} {self.mode_name}')



    # Called when CTRL-C is received
    def _CtrlCHandler(self, signum, frame):
        self.Close()



    # Determine the correct parameters for the new display
    def _GenerateXrandrParams(self, hres, vres, freq):
        # Get the raw parameter line
        try:
            mode_output = RunCommand(f'cvt {hres} {vres} {freq}').split('\n')[1]
        except IndexError:
            raise VirtualDisplayError('Unable to determine display parameters')

        # Parse out the mode parameters
        mode_params = re.findall('(?<=Modeline ).*', mode_output)[0].replace('"','')
        
        # Strip off the generated mode name, since it just causes trouble
        # (This is the first part of the parameter string)
        mode_params = mode_params.replace(mode_params.split()[0], '').strip()

        return mode_params



class VirtualDisplayError(Exception):
    def __init__(self, message):
        self.message = message
