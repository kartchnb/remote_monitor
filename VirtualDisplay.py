import re

from RunCommand import RunCommand


# TODO: Move run_command functionality out of this class
# TODO: See if we an remove all system calls and do this organically


class VirtualDisplay:
    
    def __init__(self, display_num, hres, vres, freq):
        # Determine the output name
        output_name = f'VIRTUAL{display_num}'
        self.output_name = output_name

        # Determine the parameters for the new display
        mode_name = f'{hres}x{vres}_{freq}'
        mode_params = self._GenerateXrandrParams(hres, vres, freq)
        
        # TODO: Need to check if the display mode already exists first!
        # TODO: If we try to recreate an existing display mode, xrandr errors

        # Create the new display mode
        RunCommand(f'xrandr --newmode {mode_name} {mode_params}')

        # Add the display mode for the requested output
        RunCommand(f'xrandr --addmode {output_name} {mode_name}')

        # Enable the requested output using the new display mode
        RunCommand(f'xrandr --output {output_name} --mode {mode_name}')



    # Determine the correct parameters for the new display
    def _GenerateXrandrParams(self, hres, vres, freq):
        # Get the raw parameter line
        try:
            mode_output = RunCommand(f'cvt {hres} {vres} {freq}').split('\n')[1]
            print(mode_output)
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



if __name__ == '__main__':
    import sys

    try:
        display_num = sys.argv[1]
    except IndexError:
        display_num = 1

    try:
        hres = sys.argv[2]
    except IndexError:
        hres = 960

    try:
        vres = sys.argv[3]
    except IndexError:
        vres = 600

    try:
        freq = sys.argv[4]
    except IndexError:
        freq = 60

    try:
        print(f'Configuring virtual display {display_num} for {hres}x{vres} at {freq} Hz')
        virtualDisplay = VirtualDisplay(display_num, hres, vres, freq)
    except VirtualDisplayError as e:
        print(f'VirtualDisplay Error: {e.message}')
