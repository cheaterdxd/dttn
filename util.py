from pathlib import Path

from pwnlib.tubes.process import process
import importFile
from executeCommand import executeOnce
from formatOutput.prettyAnnounce import bcolors, log


def is_path_exist(path):
    return Path(path).exists()

def clean_terminal():
    # importFile.os.system('reset')
    print('\033[2J')
    print('\033[0;0H')

def stop_terminal():
    input('Nhấn phím bất kì để tiếp tục')

# prefix components:
space =  '    '
branch = f'{bcolors.WARNING}│{bcolors.ENDC}   '
# pointers:
tee =    f'{bcolors.WARNING}├──{bcolors.ENDC} '
last =   f'{bcolors.WARNING}└──{bcolors.ENDC} '

def tree_in_verbose(dir_path: Path, prefix: str=''):
    """A recursive generator, given a directory Path object
    will yield a visual tree structure line by line
    with each line prefixed by the same characters
    """    
    contents = list(dir_path.iterdir())
    # contents each get pointers that are ├── with a final └── :
    pointers = [tee] * (len(contents) - 1) + [last]
    for pointer, path in zip(pointers, contents):
        if(path.is_dir()):
            yield prefix + pointer + bcolors.OKCYAN + path.name + bcolors.ENDC
            extension = branch if pointer == tee else space 
            # i.e. space because last, └── , above so no more |
            yield from tree_in_verbose(path, prefix=prefix+extension)
        else:
            yield prefix + pointer + path.name
        # if path.is_dir(): # extend the prefix and recurse:
            
def tree_dir(dir_path: Path, prefix: str=''):
    """A recursive generator, given a directory Path object
    will yield a visual tree structure line by line
    with each line prefixed by the same characters
    """    
    contents = list(dir_path.iterdir())
    # contents each get pointers that are ├── with a final └── :
    pointers = [tee] * (len(contents) - 1) + [last]
    for pointer, path in zip(pointers, contents):
        if(path.is_dir()):
            yield prefix + pointer + bcolors.OKCYAN + path.name + bcolors.ENDC
        else:
            yield prefix + pointer + path.name

def list_dir(path):
    # print(os.listdir(path))
    # for c in Path(path).iterdir():
    #     if(c.is_dir()==True):
    #         print(c.absolute())
    #         list_dir(c.absolute())
    for line in tree_dir(Path(path)):
        print(line)

def list_dir_verbose(path):
    for line in tree_in_verbose(Path(path)):
        print(line)

def list_process():
    '''
    Liệt kê các tiến trình đang chạy trong hệ điều hành
    return: danh sách các tiến trình đang hiện có -> List
    return: -1 nếu quá trình lấy thông tin lỗi -> Bool
    return: -2 nếu hệ điều hành không phải linux -> Int
    '''
    if(importFile.os_type.upper()=='Linux'.upper()):
        command = 'ps -aux'
        reponse = executeOnce(command)
        if(reponse.returncode == 0):
            return reponse.stdout.decode().split("\n")
        else:
            return -1
    else:
        return -2

def list_ext_at_path(path, ext):
    '''
        Liệt kê file nằm ở đường dẫn path có đuôi .[ext]
        parm1 path: đường dẫn tìm kiếm
        parm2 ext: đuôi file tìm kiếm
    '''
    import glob
    log.info(f"Tìm kiếm *.{ext} trong thư mục {path}")
    list_f_response = glob.glob(f'{path}/*.{ext}')
    return list_f_response

def list_ext_at_path_by_root(root,path, ext):
    '''
        Liệt kê file nằm ở đường dẫn path có đuôi .[ext]
        parm1 path: đường dẫn tìm kiếm
        parm2 ext: đuôi file tìm kiếm

        return:
        danh sách các dòng trả về 
    '''
    find_cmd = f'find {path} -type f -name "*.{ext}"'
    resp = root_do_and_response(root,find_cmd)
    return resp.split('\n')

def list_process_as_root(root_talk):
    '''
    Liệt kê các tiến trình đang chạy bằng quyền root
    return: -1 nếu hệ điều hành không phải linux -> Int 
    return: danh sách tiến trình nếu thành công -> List
    '''
    if(importFile.os_type.upper()=='Linux'.upper()):
        process_list = []

        root_talk.sendline("ps -aux")
        while(True):
            out = root_talk.recvline(timeout=0.3).strip(b'\n').decode()
            if(out==''):
                break
            process_list.append(out)
        return process_list

    else:
        return -1
    
def leak(name,root_talk):
    '''
    Lấy thông tin file shadow hoặc passwd
    return:
    -1 : nếu file không phải là shadow, passwd
    [] : danh sách lines trong file
    '''
    if(name not in ['shadow','passwd']):
        return -1
    else:

        user_l = []
        root_talk.sendline(f'cat /etc/{name}')
        while(True):
            out = root_talk.recvline(timeout=0.3).strip(b'\n').decode()
            if(out==''):
                break
            user_l.append(out)
        return user_l

is_done = 0
def waiting_bar():
    import time
    global is_done
    while(not is_done):
        # size = os.path.getsize(path) 
        # print('Size of file is', size, 'bytes\n')
        # time.sleep(0.5)
        log.print_it_out(bcolors.OKGREEN,"[o][ ][ ][ ]"," Đang tải về tệp tin vá lỗi ...",'\r')
        time.sleep(0.5)
        log.print_it_out(bcolors.OKGREEN,"[ ][o][ ][ ]"," Đang tải về tệp tin vá lỗi ...",'\r')
        time.sleep(0.5)
        log.print_it_out(bcolors.OKGREEN,"[ ][ ][o][ ]"," Đang tải về tệp tin vá lỗi ...","\r")
        time.sleep(0.5)
        log.print_it_out(bcolors.OKGREEN,"[ ][ ][ ][o]"," Đang tải về tệp tin vá lỗi ...",'\r')
        time.sleep(0.5)

def download_file(url,file_name,file_container):
    '''
    download file from url
        + filename : name of file use after completed
        + file_container: parent folder path of the file
    '''
    import requests
    import threading
    log.info(f"Tải tệp từ {url} , lưu vào {file_container}")
    global is_done
    try:
        x = threading.Thread(target=waiting_bar)
        x.start()
        r = requests.get(url,allow_redirects=True)
        with open(file_container+'/'+file_name,'wb') as inf:
            inf.write(r.content)
        is_done = 1
        while(x.is_alive()==False):
            continue
        return 1
    except:
        return -1

def decompress_gz(file_path,dest=""):
    '''
      giải nén tệp tin

            file_path: đường dẫn tới file
            dest: đường dẫn tới thư mục muốn giải nén, mặc định là tại chỗ 
    '''
    if(is_path_exist(file_path)):
        if(dest!=''):
            option = '-C'
        else:
            option = ''
        resp = executeOnce(f"tar xfz {file_path} {option} {dest}")
        print(resp)
        return resp.returncode
    else:
        log.fail(f"Không tìm thấy tệp tin {file_path}")
    
def print_check_stdout_stderr(arg):
    stdout_s = arg.stdout.decode()
    stderr_s = arg.stderr.decode()
    print(stdout_s+'\n'+stderr_s)
    if(stderr_s!='' and not 'warning' in stderr_s and not "WARNING" in stderr_s):
        log.fail(stderr_s)


def root_do_and_response(root:process,cmd):
    '''
    root thực hiện lệnh và trả về 
    output: 
    str, nếu câu lệnh trả về
    '', nếu câu lệnh không trả về
    '''

    all_o = b''
    root.sendline(cmd)
    while(True):
        out1 = root.recv(1,timeout=0.3)
        all_o += out1
        if(len(out1) < 1):
            break
    return all_o.decode('latin-1')

def yes_no_ask(ques):
    '''
    confirm lựa chọn exit, delete,...
        ques: câu hỏi sẽ hỏi

        y: return 1
        n: return -1
    '''
    log.warning(ques)
    is_input_fail = True
    while(is_input_fail):
        ans = str(input("[y/n]  ").strip('\n'))
        if(ans.lower() == 'y'):
            return 1
        elif ans.lower() == 'n':
            return -1
        else:
            log.fail("Nhập sai lựa chọn, chỉ y/Y (có) hoặc n/N (không).")

def up_root_for_exist_user(root_talk, username:str):
    '''
    Nâng quyền cho một người dùng đã tồn tại có quyền root

    parm 1: root_talk: tiến trình root đã tạo
    parm 2: username: tên người dùng muốn nâng quyền

    return 
        0 nếu thành công
        -1 nếu thất bại
    '''
    command = f"echo '{username}    ALL=(ALL) ALL' >> /etc/sudoers"

    root_talk.sendline(command)
    root_talk.sendline('tail -1 /etc/sudoers')
    while(True):
        out = root_talk.recvline(timeout=0.3).strip(b'\n').decode()
        if(out==''):
            break
        if f'{username}    ALL=(ALL) ALL' in out:
            return 0

    return -1
