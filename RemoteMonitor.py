import notify2
import socket
import subprocess

from RunCommand import RunCommand
from VirtualDisplay import VirtualDisplay, VirtualDisplayError
from VncDisplay import VncDisplay, VncDisplayError



class RemoteMonitor():

    def __init__(self, displayNum, hres, vres, freq, ncache=0):
        # Initialize the notify interface
        notify2.init('Remote Monitor Test')

        # Create a virtual display for the remote monitor
        try:
            virtualDisplay = VirtualDisplay(displayNum, hres, vres, freq)
            outputName = virtualDisplay.output_name
        except VirtualDisplayError as e:
            raise RemoteMonitorError(e.message)

        # Prompt the user to adjust the display location before continuing
        self._Notify('Adjust the remote monitor location and close the display settings window when done')
        subprocess.run('xfce4-display-settings')

        # Create a VNC display for the remote monitor
        try:
            vncDisplay = VncDisplay(outputName, ncache)
        except VncDisplayError as e:
            raise RemoteMonitorError(e.message)

        # Let the user know that the remote monitor is ready to be connected
        address = self._GetAddress()
        self._Notify(f'The remote monitor is ready at ip address {address}')



    # Send a notification to the desktop and the console
    def _Notify(self, message):
        notify2.Notification('Remote Monitor', message).show()
        print(message)



    def _GetAddress(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        try:
            # Attempt to contact a remote IP address (it does not have to be reachable)
            s.connect(('10.255.255.255', 1))
            address = s.getsockname()[0]
        
        except Exception:
            # Try a different method that doesn't work as well
            address = socket.gethostbyname(socket.gethostname())
        
        finally:
            s.close()
        
        return address




class RemoteMonitorError(Exception):
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
        print(f'Configuring remote monitor using virtual display {display_num} with resolution of {hres}x{vres} at {freq} Hz')
        RemoteMonitor = RemoteMonitor(display_num, hres, vres, freq)
    except RemoteMonitorError as e:
        print(f'RemoteMonitor Error: {e.message}')
