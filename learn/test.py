from pathlib import Path
import shlex, subprocess as subpr
import os


def findext():
    import glob
    list_f_response = glob.glob('/home/cheaterdxd/dttn/*',recursive=True)
    for f in list_f_response:
        print(f)


def executeOnce(command):
    '''
        Thực thi lệnh 1 lần và lấy trả về của lệnh
        args: command in one line
        return: output of command
    '''

    args_l = shlex.split(command)
    # print(command)
    return subpr.run(command,stdout=subpr.PIPE, stderr=subpr.PIPE,shell=True)
def is_path_exist(path):
    return Path(path).exists()

def decompress_gz(file_path,dest=""):
    '''
      giải nén tệp tin

            file_path: đường dẫn tới file
            dest: đường dẫn tới thư mục muốn giải nén, mặc định là tại chỗ 
    '''
    print(os.getcwd())
    print(file_path)
    if(is_path_exist(os.getcwd()+"/"+file_path)):
        resp = executeOnce(f"tar -xzf {file_path}")
        print(resp)
        return resp.returncode 
    else:
        print('not found')
  
# findext()
# decompress_gz('patched.tar.gz','patched_dir/')
os.chdir('/home/tuan/dttn/linux/cve_2021_3156/patched_dir/sudo-1.9.5p2/')
print(executeOnce("sudo make").stdout.decode())