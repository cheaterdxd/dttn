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

def menu_header(header:str,break_len):
    out_format_head = ''
    import textwrap
    te = textwrap.wrap(header,break_len,break_long_words=False)
    out_format_head+=('┌'+'─'*(break_len+2)+'┐')
    out_format_head+= '\n'
    for line in te:
        align_len = int((break_len+2 - len(line))/2)
        align_text = align_len*' '+line+align_len*' '
        align_text = align_text.ljust(break_len+2,' ')
        out_format_head+=('│'+align_text+'│')+'\n'
    out_format_head+=('└'+'─'*(break_len+2)+'┘')+'\n'
    return out_format_head
from pwn import *
def try_read_stdout():
    s = process('/bin/sh')
    cmd = ""
    while(True):
        cmd = str(input('>>> ').strip('\n'))
        if(cmd != 'exit'):
            print("thực hiện câu lệnh: "+cmd)
            s.sendline(cmd)
            out_all =b''
            while(True):
                ret1 = (s.recv(1,timeout=0.3))
                print('debug ', ret1)
                out_all += ret1
                if(len(ret1) < 1):
                    # out_all+=ret1
                    # print(ret1.decode())
                    # print(len(ret1))
                    break
            print(out_all.decode())
        else:
            break
# try_read_sudoers()
# print(menu_header("Ứng dụng khai thác lỗ hổng phần mềm made by le thanh tuan",20))
# try_read_stdout()
"""
def tree_dir_in_verbose(dir_path: Path, prefix: str=''):    
    contents = list(dir_path.iterdir())
    # contents each get pointers that are ├── with a final └── :
    pointers = [tee] * (len(contents) - 1) + [last]
    for pointer, path in zip(pointers, contents):
        if(path.is_dir()):
            yield prefix + pointer + bcolors.OKCYAN + path.name + bcolors.ENDC
            extension = branch if pointer == tee else space 
            # i.e. space because last, └── , above so no more |
            yield from tree_dir_in_verbose(path, prefix=prefix+extension)
        else:
            yield prefix + pointer + path.name
        # if path.is_dir(): # extend the prefix and recurse:
            
def tree_dir(dir_path: Path, prefix: str=''):
ch line prefixed by the same characters

    contents = list(dir_path.iterdir())
    # contents each get pointers that are ├── with a final └── :
    pointers = [tee] * (len(contents) - 1) + [last]
    for pointer, path in zip(pointers, contents):
        if(path.is_dir()):
            yield prefix + pointer + bcolors.OKCYAN + path.name + bcolors.ENDC
        else:
            yield prefix + pointer + path.name

def tree_dir(root_talk:process,path):
    '''
    liệt kê tất cả các tệp trong 1 thư mục
    
    return: []
    '''
    command = f'ls -l {path}'
    resp = root_do_and_response(root_talk,command)
    list_f = resp.split('\n')

def list_dir(path):
    # print(os.listdir(path))
    # for c in Path(path).iterdir():
    #     if(c.is_dir()==True):
    #         print(c.absolute())
    #         list_dir(c.absolute())
    for line in tree_dir(Path(path)):
        print(line)

def list_dir_verbose(path):
    for line in tree_dir_in_verbose(Path(path)):
        print(line)
"""

def parsing_line_ls(line:str)-> list:

    line = line.split(' ')

    while('' in line):
        idx = line.index('')
        del line[idx]
    return [line[0], line[8]]

def try_read_ls(path:str):
    import subprocess as subpr
    cmd = f'ls -l {path}'
    resp = subpr.run(cmd,stdout=subpr.PIPE,shell=True)
    chia_enter = (resp.stdout.decode().split("\n"))
    list_out =[]
    del chia_enter[0]
    del chia_enter[len(chia_enter)-1]
    for line_enter in chia_enter:
        # print(line_enter)
        name_and_type = parsing_line_ls(line_enter)
        list_out.append(name_and_type)
    return list_out

def color_ls(list_in:list):
    for i in list_in:
        if('d' == i[0][0]):
            print('xanh '+i[1])
        else:
            print('xam '+i[1])

def ls_verbose(path:str):
    import subprocess as subpr
    cmd = f'ls -l -R {path}'
    resp = subpr.run(cmd,stdout=subpr.PIPE,shell=True)
    folder_split = (resp.stdout.decode().split("\n\n"))
    dict_dir = {}
    dict_dir['root_path'] = path
    for i in (folder_split):
        # print(i)
        # print('end =============================================================')
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
def color_verbose_ls(dict_dir:dict,root_path:str,indent):
    level_prefix = ('│'if indent>0 else '')+indent*'    ' + ('└──' if indent>0 else "")
    print(level_prefix + root_path)
    sub_of_root = dict_dir[root_path] # a list
    

    for sub in sub_of_root:
        new_indent=indent+1
        if sub[0][0] == 'd':
            
            color_verbose_ls(dict_dir,root_path+'/'+sub[1],new_indent)
        else:
            print(('│'if (new_indent)>0 else '')+'    '*(new_indent)+('└──' if new_indent>0 else "")+ sub[1])

space =  '    '
branch = f'│  '
# pointers:
tee =    f'├── '
last =   f'└── '
def color_verbose_ls2(dict_dir:dict,root_path:str,prefix = ''):
    # print("current prefix :" + prefix)
    global branch, space, tee, last
    print(prefix +tee+ root_path)
    sub_of_root = dict_dir[root_path] # a list
    for sub in sub_of_root:
        if sub[0][0] == 'd':
            prefix_next = branch +prefix+ space
            color_verbose_ls2(dict_dir,root_path+'/'+sub[1],prefix_next)
        else:
            print(prefix+ sub[1])



# color_ls(try_read_ls('/'))
color_verbose_ls(ls_verbose('/home/cheaterdxd/dttn/linux'),'/home/cheaterdxd/dttn/linux',0)
