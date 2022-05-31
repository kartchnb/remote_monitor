import re
import signal

from RunCommand import RunCommand


# TODO: Move run_command functionality out of this class
# TODO: See if we an remove all system calls and do this organically


class VirtualDisplay:

    # The maximum virtual display number to support
    _maxDisplayNum = 9

    # Standard frequency for all remote monitors
    _frequency = 60
    
    def __init__(self, display_num, hres, vres):
        # Determine the output name
        output_name = f'VIRTUAL{display_num}'
        self.output_name = output_name

        # Determine the parameters for the new display
        mode_name = f'{hres}x{vres}_{self._frequency}'
        self.mode_name = mode_name
        mode_params = self._GenerateXrandrParams(hres, vres, self._frequency)

        # TODO: Need to check if the display mode already exists first!
        # TODO: If we try to recreate an existing display mode, xrandr errors

        # Create the new display mode
        RunCommand(f'xrandr --newmode {mode_name} {mode_params}')

        # Add the display mode for the requested output
        RunCommand(f'xrandr --addmode {output_name} {mode_name}')

        # Enable the requested output using the new display mode
        RunCommand(f'xrandr --output {output_name} --mode {mode_name}')

        # Add a handler for CTRL-C
        signal.signal(signal.SIGINT, self._CtrlCHandler)



    def __del__(self):
        self.Close()



    # Close the virtual display
    def Close(self):
        output_name = self.output_name
        mode_name = self.mode_name

        # Delete the virtual display
        RunCommand(f'xrandr --output {output_name} --off')
        RunCommand(f'xrandr --delmode {output_name} {mode_name}')



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
