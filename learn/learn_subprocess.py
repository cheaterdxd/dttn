import subprocess

# subprocess.run('ls')
# subprocess.run('ls -la' , shell=True)


# new_ls_process = subprocess.Popen(['ls', '-la'], stdout=subprocess.PIPE, stdin=subprocess.PIPE)

# print(new_ls_process.communicate()[0].decode())

'''communicate with other subprocess'''
# getNameApp = subprocess.Popen(['python3','interactive.py'],stdin=subprocess.PIPE, stdout=subprocess.PIPE)
# output = getNameApp.communicate(b'le thanh tuan')
# print(output[0].decode())
