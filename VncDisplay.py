import re

from RunCommand import RunCommand



class VncDisplay():

    def __init__(self, output_name, port=5900):
        clip_area = self._DetermineClipArea(output_name)
        self._LaunchVnc(clip_area, port)



    def _DetermineClipArea(self, output_name):
        xrandr_output = RunCommand('xrandr')

        try:
            output_string = re.findall(f'{output_name}.*', xrandr_output)[0]
        except IndexError:
            raise VncDisplayError(f'Could not find output named "{output_name}"')

        try:
            output_params = output_string.split()
            connected = output_params[1] == 'connected'
            clip_area = output_params[2]
        except IndexError:
            raise VncDisplayError(f'The parameters for "{output_name}" were malformed\nRead in "{output_string}"')

        if not connected:
            raise VncDisplayError(f'Output "{output_name}" is not connected')

        return clip_area



    def _LaunchVnc(self, clip_area, port):
        #command = f'x11vnc -clip {clip_area} -rfbport {port} -repeat -forever'
        command = f'x11vnc -clip {clip_area} -rfbport {port}'

        print(f'Launch VNC with command: {command}')
        RunCommand(command)



class VncDisplayError(Exception):
    def __init__(self, message):
        self.message = message
