from menu_list import cve_menu, entry_dynamic_menu
from findInfoSystem import get_system_info,is_Linux
from util import clean_terminal, stop_terminal
import importlib
from importFile import sys, signal
import importFile
from formatOutput import prettyAnnounce
logf = prettyAnnounce.log
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
        logf.warning("vui lòng nâng cấp lên python 3, tốt nhất là từ 3.6.9 trở lên")
    elif(num2_ver<'6'):
        logf.warning("chương trình có thể chạy không chính xác ở phiên bẳn python hiện tại, tốt nhất là từ 3.6.9 trở lên")
    elif(num3_ver<'9'):
        logf.warning("chương trình có thể chạy không chính xác ở phiên bẳn python hiện tại, tốt nhất là từ 3.6.9 trở lên")
def main():
    
    if(is_Linux()==False):
        logf.fail("Hệ thống của bạn không phải Linux! Các chức năng dành cho Windows chưa được triển khai!")
        exit(1)
    else:
        importFile.os_type = 'linux'
    signal.signal(signal.SIGINT, signal_handler)
    check_before_run()
    while(1):
        clean_terminal()
        main_menu_func = ['Xem thông tin hệ thống','Kiểm tra CVE']
        choice_in_menu = entry_dynamic_menu(main_menu_func,len(main_menu_func),">>>",symbols_color=prettyAnnounce.bcolors.OKGREEN,
        header="ỨNG DỤNG KHAI THÁC LỖ HỔNG LINUX\n LÊ THANH TUẤN")
        if(choice_in_menu == '1'):
            clean_terminal()
            get_system_info()
            stop_terminal()
        elif choice_in_menu == '2':
            choose_in_cve_menu = cve_menu()
            if(choose_in_cve_menu!=None):
                do_cve(choose_in_cve_menu)
        elif choice_in_menu == '0':
            exit()


if __name__ == "__main__":
    main()
