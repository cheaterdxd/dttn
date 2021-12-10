from pathlib import Path

from pwnlib.tubes.process import process

import importFile
from executeCommand import executeOnce
from formatOutput.prettyAnnounce import bcolors, log


def is_path_exist(path):
    return Path(path).exists()
def is_dir(root_talk:process, path:str)->int:
    '''
    Kiểm tra path có phải đường dẫn thật tồn tại không?
    return 1: đúng là 1 đường dẫn tồn tại
    return 0: không tồn tại hoặc không phải đường dẫn
    '''
    cmd = f'test -d {path} && echo 1 || echo 0'
    resp = root_do_and_response(root_talk,cmd).strip('\n')
    return (1 if(resp == '1') else 0)

def is_file_exist(root_talk:process, path:str)->int:
    '''
    Kiểm tra path có phải đường dẫn thật tồn tại không?
    return 1: đúng là 1 đường dẫn tồn tại
    return 0: không tồn tại hoặc không phải đường dẫn
    '''
    cmd = f'test -f {path} && echo 1 || echo 0'
    resp = root_do_and_response(root_talk,cmd).strip('\n')
    return (1 if(resp == '1') else 0)

def clean_terminal():
    # importFile.os.system('reset')
    print('\033[2J')
    print('\033[0;0H')

def stop_terminal():
    input('Nhấn phím bất kì để tiếp tục')

# prefix components:
space =  '    '
branch = f'{bcolors.WARNING}│{bcolors.ENDC}'
# pointers:
tee =    f'{bcolors.WARNING}├──{bcolors.ENDC}'
last =   f'{bcolors.WARNING}└──{bcolors.ENDC}'

def parsing_line_ls(line:str)-> list:
    '''
    Sử dụng để trích xuất từ dòng của ls command
    '''
    line = line.split(' ')

    while('' in line):
        idx = line.index('')
        del line[idx]
    return [line[0], line[8]]

def ls_normal(root_talk:process, path:str)->list:
    '''
    thực thi ls -l [path] 
    retunr:
    list các tệp trong đường dẫn
    '''
    cmd = f'ls -l {path}'
    resp = root_do_and_response(root_talk,cmd)
    chia_enter = resp.split('\n')
    list_out =[]
    del chia_enter[0]
    del chia_enter[len(chia_enter)-1]
    for line_enter in chia_enter:
        # print(line_enter)
        name_and_type = parsing_line_ls(line_enter)
        list_out.append(name_and_type)
    return list_out

def color_ls(list_in:list):
    '''
    tô màu và in ra kết quả
    '''
    for i in list_in:
        if('d' == i[0][0]):
            print(f'{last}{bcolors.OKCYAN}{i[1]}{bcolors.ENDC}')
        else:
            print(f'{last}{i[1]}')

def ls_verbose(root_talk: process, path:str)->dict:
    '''
    thực thi ls -l -R [path] : liệt kê đệ quy các thư mục trong đường dẫn
    retunr:
    dict: các tệp trong đường dẫn
    '''
    cmd = f'ls -l -R {path}'
    resp = root_do_and_response(root_talk,cmd)
    folder_split = (resp.split("\n\n"))
    dict_dir = {}
    dict_dir['root_path'] = path
    for i in (folder_split):
        enter_split  = i.split('\n')
        name = enter_split[0][0:-1]
        del enter_split[0] # del name
        del enter_split[0] # del total line
        element_in_folder = []
        for line_enter_split in enter_split:
            if line_enter_split != '':
                name_and_type = parsing_line_ls(line_enter_split)
                element_in_folder.append(name_and_type)
        dict_dir[name] = element_in_folder
    return dict_dir

def color_verbose_ls(dict_dir:dict,root_path:str,indent=0):
    '''
    tô màu cho liệt kê đệ quy
    indent: 0 ở vòng root
    '''
    # print(dict_dir)
    level_prefix = (branch if indent>0 else '')+indent*space + (last if indent>0 else "")
    print(f'{level_prefix} {bcolors.OKCYAN}{root_path}{bcolors.ENDC}')
    sub_of_root = dict_dir[root_path] # a list
    for sub in sub_of_root:
        new_indent=indent+1
        if sub[0][0] == 'd':
            color_verbose_ls(dict_dir,root_path+'/'+sub[1],new_indent)
        else:
            print((branch if (new_indent)>0 else '')+space*(new_indent)+(tee if new_indent>0 else "")+ sub[1])

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
    import threading

    import requests
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

def root_do_and_response(root:process,cmd)->str:
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

def copy_file(root_talk:process, file_source:str, dest:str):
    '''
    Sao chép file từ file_source sang thư mục dest
    '''
    cmd = f'cp {file_source} {dest}'
    root_do_and_response(root_talk,cmd)

def copy_all_folder(root_talk:process, dir_source:str, dest:str):
    '''
    Sao chép thư mục từ dir_source sang thư mục dest
    '''
    cmd = f'cp -R {dir_source} {dest}'
    root_do_and_response(root_talk,cmd)

def ask_input_string(ask:str)->str:
    '''
    Hỏi nhập và trả về answer
    '''
    ans = ''.join(str(input(f'{ask}\n>>> ')).split())
    return ans

def ask_input_int_inrange(ask:str, from_:int, to_:int)->int:
    '''
    Hỏi yêu cầu nhập số trong khoảng từ from_ đến to_
    '''
    is_loop = False
    ext_choice = -1
    # check input
    while(not is_loop):
        try:
            ext_choice = int(''.join(str(input(f"{ask}\n>>> ")).split()),10)
            if(ext_choice >= from_ and ext_choice <= to_):
                # đÚng
                is_loop = True
            else:
                log.fail("Bạn đã nhập sai giá trị. Mời nhập lại!")
        except ValueError:
            log.fail("Chỉ nhập số để lựa chọn!")
    return ext_choice