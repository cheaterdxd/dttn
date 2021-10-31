from .checkVersion import is_Linux
from formatOutput import prettyAnnounce as prAn
from checkSudo import subprocess
def check_vuln():
    is_vuln = False
    if(is_Linux()==False):
        prAn.log.fail("Hệ thống của bạn không phải linux ! Thoát chương trình !")
        exit(1)
    else:
        error_key = b'malloc():'
        
        for i in range(0,500):
            output = subprocess.run(["/usr/bin/sudoedit",'-s','aaaaaaaaaaaaaaa\\','b'*i],capture_output=True)
            if(error_key in output.stderr or error_key in output.stdout):
                is_vuln = True
                break
        return is_vuln
