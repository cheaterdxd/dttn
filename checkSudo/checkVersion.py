from checkSudo import platform, subprocess
# from importFile import platform , subprocess as subpr
def check_version():
    command = ['sudo', '-V']
    output = subprocess.run(command,capture_output=True)
    print(output.stdout.decode())

def is_Linux():
    if(platform.system() == "Linux"):
        return True
    else:
        return False


