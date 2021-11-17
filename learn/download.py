import requests
import os
import threading
import time
is_done = 0
def get_file_stat(path):
    i = 0
    while(not is_done):
        # size = os.path.getsize(path) 
        # print('Size of file is', size, 'bytes\n')
        # time.sleep(0.5)
        print("[o][ ][ ][ ] downloading...",end='\r')
        time.sleep(0.5)
        print("[ ][o][ ][ ] downloading...",end='\r')
        time.sleep(0.5)
        print("[ ][ ][o][ ] downloading...",end='\r')
        time.sleep(0.5)
        print("[ ][ ][ ][o] downloading...",end='\r')
        time.sleep(0.5)


url = 'https://www.sudo.ws/dist/sudo-1.9.5p2.tar.gz'
file_name = 'sudo-1.9.5p2.tar.gz'
try:
    asf = open(file_name,'w')
    asf.close()
    x = threading.Thread(target=get_file_stat,args=(file_name,))
    x.start()
    time.sleep(0.1)
    time.sleep(20)
    is_done = 1
except:
    print("error")
print("code session")
# r = requests.get(url,allow_redirects=True)
# print('\n'+r.headers.get('Content-Length'))
# # print(r.headers.get('Content-Disposition'))
# with open(file_name,'wb') as in_f:

#     in_f.write(r.content)
#     is_done = 1


    




