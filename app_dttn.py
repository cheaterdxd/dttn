from menu_list import cve_menu, main_menu
from findInfoSystem import get_system_info
from util import clean_terminal
import importlib
from importFile import sys, signal
from formatOutput import prettyAnnounce

def signal_handler(signal, frame):
    print('\nBạn đã thoát chương trình bằng Ctrl+C. Hẹn gặp lại. ')
    sys.exit(0)



def run_entry_for_cve(module_name):
    # load the module, will raise ImportError if module cannot be loaded
    m = importlib.import_module(module_name)
    # get the class, will raise AttributeError if class cannot be found
    c = getattr(m, 'entry')
    return c

def do_cve(cve_name):
    cl = (run_entry_for_cve(f'linux.{cve_name}.{cve_name}'))
    cl() # call cve entry

def check_before_run():
    '''
    Co dung phien ban python3.6 
    Co cai pwntools chua? 
    '''
    ver = sys.version.split(" ")[0].split('.')
    print(ver)
    num1_ver = ver[0]
    num2_ver = ver[1]
    num3_ver = ver[2]
    if(num1_ver!='3'):
        prettyAnnounce.log.warning("vui lòng nâng cấp lên python 3, tốt nhất là từ 3.6.9 trở lên")
    elif(num2_ver<'6'):
        prettyAnnounce.log.warning("chương trình có thể chạy không chính xác ở phiên bẳn python hiện tại, tốt nhất là từ 3.6.9 trở lên")
    elif(num3_ver<'9'):
        prettyAnnounce.log.warning("chương trình có thể chạy không chính xác ở phiên bẳn python hiện tại, tốt nhất là từ 3.6.9 trở lên")
def main():
    signal.signal(signal.SIGINT, signal_handler)
    check_before_run()
    while(1):
        clean_terminal()
        choice = main_menu()
        if(choice == '1'):
            clean_terminal()
            get_system_info()
            input('Ấn Enter để thoát ra menu')
        elif choice == '2':
            choose = cve_menu()
            if(choose!=None):
                do_cve(choose)
        elif choice == '3':
            exit()
    
    # run_exploit.run()
    # list_dir('/home/cheaterdxd')
    # list_dir_verbose('/home/cheaterdxd/dttn/')
    # list_process()




if __name__ == "__main__":
    main()
