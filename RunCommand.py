import subprocess

# Make the process of running a system command and getting the output simpler
def RunCommand(command):
    command_array = command.split()
    return subprocess.run(command_array, stdout=subprocess.PIPE).stdout.decode()
