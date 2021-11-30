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
def check_stdout_stderr(arg):
    stdout_s = arg.stdout.decode()
    stderr_s = arg.stderr.decode()
    print(stdout_s+'\n'+stderr_s)

    if(stderr_s!=''):
        print("==============================fail at " + stderr_s)

def do_the_fix():
    '''
    1.kiem tra ton tai thu muc cai dat ? xoa : tao moi
    1.1 di den thu muc cai dat
    2.download tep cai dat
    3.kiem tra tep cai dat da download thanh cong chua? <go to giai nen>:<go to download again>
    4. giai nen
    4.1 di den thu muc giai nen ra
    5. thuc hien cac buoc cai dat <kiem tra ki cang output thanh cong>

    '''
    destionation_path = '/home/tuan/dttn/linux/cve_2021_3156'
    decompress_folder = 'patched_dir'
    file_name = 'sudo-1.9.5p2.tar.gz'
    extract_patched_folder = 'sudo-1.9.5p2'
    if is_path_exist(destionation_path+'/'+decompress_folder)==False:
        print('================== tao thu muc moi ====================')
        os.mkdir(destionation_path+'/'+decompress_folder)
    os.chdir(destionation_path+'/'+decompress_folder)
    if(not is_path_exist(destionation_path+'/'+decompress_folder+'/'+file_name)):
        print("not download done yet !")
    else:
        print('================== thu muc giai nen ton tai ====================')
        os.chdir(destionation_path+'/'+decompress_folder+'/'+extract_patched_folder)
        check_stdout_stderr(executeOnce('sudo apt-get update'))
        check_stdout_stderr(executeOnce("sudo apt-get install make"))
        check_stdout_stderr(executeOnce('sudo apt-get install build-essential'))
        check_stdout_stderr(executeOnce('sudo ./configure'))
        check_stdout_stderr(executeOnce('sudo make'))
        check_stdout_stderr(executeOnce('sudo make install'))


# findext()
# decompress_gz('patched.tar.gz','patched_dir/')
# os.chdir('/home/tuan/dttn/linux/cve_2021_3156/patched_dir/sudo-1.9.5p2/')
# print(executeOnce("sudo make").stdout.decode())
# do_the_fix()
def try_read_sudoers():
    with open('/etc/sudoers','r') as fs:
        print(fs.readlines(10))

try_read_sudoers()