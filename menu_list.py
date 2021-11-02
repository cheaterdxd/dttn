'''
Các menu của chưƠng trình, xử lý nhận input và return input
'''

from findInfoSystem import is_Linux
from formatOutput import prettyAnnounce as logf
import importFile
from pathlib import Path

def main_menu():
    color = logf.bcolors
    print(f"{color.WARNING}=========================================================={color.ENDC}")
    print("||    Công cụ khai thác cve 2021-3156 phiên bản 1.0     ||",end='\n')
    print(f"{color.WARNING}=========================================================={color.ENDC}")
    # print("Thông tin hệ thống: ",end='\n')
    # info.new_get_system_info()
    if(is_Linux()==False):
        logf.log.fail("Hệ thống của bạn không phải Linux! Các chức năng dành cho Windows chưa được triển khai!")
        exit(1)
    else:
        importFile.os_type = 'linux'
    while(1):
        print("Hãy chọn thao tác mong muốn\n")
        print("1. Xem thông tin hệ thống")
        print("2. Kiểm tra CVE.")
        print("3. Thoát")
        symbols_out = f'{logf.bcolors.OKGREEN}>>>{logf.bcolors.ENDC} '
        choice = str(input(symbols_out).strip('\n'))

        if(choice in ['1','2','3']):
            return (choice)
        else:
            print(end='\n')
            logf.log.fail("Lựa chọn không hợp lệ !\n")

def cve_menu():
    print(f'{logf.bcolors.WARNING}Danh sách cve hiện có{logf.bcolors.ENDC}')
    all_cve = []
    idx = 0
    print(f"    {logf.bcolors.OKCYAN}[{idx}] {logf.bcolors.ENDC}Thoát menu.")
    idx+=1
    for i in Path(importFile.root_directory + '/linux').iterdir():
        if(i.name.startswith('cve')):
            print(f"    {logf.bcolors.OKCYAN}[{idx}] {logf.bcolors.ENDC}{i.name.upper()}")
            all_cve.append(i.name.upper()) # chuẩn format cho đẹp
            idx+=1
    out_symbols = (f'\n{logf.bcolors.WARNING}(Chọn số) >>>{logf.bcolors.ENDC} ')
    while(1):
        cve_idx = int(input(out_symbols).strip('\n')) 
        if(cve_idx > len(all_cve)):
            logf.log.fail("CVE bạn chọn chưa được xây dựng! Hãy chọn một CVE trong danh sách.")
        elif(cve_idx == 0):
            break
        else:
            return str(all_cve[cve_idx-1]).lower() # lower_case

def entry_dynamic_menu(options_text: list, number_of_ques:int, symbols_:str):
    '''
    In ra một menu có form:
    Hãy chọn thao tác mong muốn

    1. options_text 1
    2. options_text 2
    ...
    0. Thoát

    symbols_  [Chờ nhập lựa chọn]

    Tham số:

    options_text    [List]:  lựa chọn dướI dạng text
    number_of_ques  [int] : số dương lớn nhất của lựa chọn 
    symbols_        [str] : biểu tưỢng chờ nhập lựa chọn
    '''
            
    symbols_out = f'{logf.bcolors.OKCYAN}{symbols_}{logf.bcolors.ENDC} '

    while(1):
        print(f"{logf.bcolors.WARNING}Hãy chọn thao tác mong muốn{logf.bcolors.ENDC}\n")
        idx = 1 # 0 là Thoát option
        for i in options_text:
            print(f"{idx}. {i}")
            idx+=1
        print("0. Thoát")
        print(end='\n')
        choice = str(input(symbols_out).strip('\n'))
        if(choice in ' '.join(str(i) for i in range(0,number_of_ques+1))):
            return (choice)
        else:
            print(end='\n')
            logf.log.fail("Lựa chọn không hợp lệ !\n")
