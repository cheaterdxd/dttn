'''
Các menu của chưƠng trình, xử lý nhận input và return input
'''
from checkSudo.checkVersion import check_version, is_Linux
from checkSudo import checkVuln
from systemInfo import findInfoSystem as info
from formatOutput import prettyAnnounce as logf


def main_menu():
    print("Công cụ khai thác cve 2021-3156 phiên bản 1.0",end='\n')
    print("Thông tin hệ thống: ",end='\n')
    info.new_get_system_info()
    if(is_Linux()==False):
        logf.log.fail("Hệ thống của bạn không phải Linux !")
        exit(1)
    while(1):
        print("Hãy chọn thao tác mong muốn\n")
        print("1. Xem thông tin hệ thống\n")
        print("2. Kiểm tra CVE 2021-3156\n")
        user_in = str(input('>>> '))

        if(user_in in ['1','2']):
            return (user_in)
        else:
            print(end='\n')
            logf.log.fail("Lựa chọn không hợp lệ !\n")

