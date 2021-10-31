from importFile import json, logging, platform, socket
from systemInfo import current_directory, prettyAnnounce as prAn , prettyParseData as prPD
# extend import re,uuid

# =========================================================================
'''khai báo biến global - global variable section - begin'''
SYS_INFO_PATH = current_directory + "/saveJson/sysInfo.json"
'''end section'''
# =========================================================================
'''khai báo các rút gọn - global alias function name section - begin'''
logf = prAn.log
pJson = prPD.print_Json
''' end section '''
# =========================================================================

def check_exist_json_info_file():
    logf.info("Đang kiểm tra tệp tin đã lưu trước đó.")
    try:
        with open(SYS_INFO_PATH,'r') as sys_fd:
            load_data = json.load(sys_fd)
            logf.done("Tệp tin tồn tại. Đọc thông tin từ tệp tin.")
            pJson(load_data)
            return 1
    except FileNotFoundError:
        logf.fail("Chưa có lịch sử khởi tạo thông tin hệ thống !")
        return 0

def get_local_IP():
    logf.info("Khởi tạo kết nối đến 8.8.8.8 để kiểm tra IP ")
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        logf.done("Khởi tạo kết nối thành công !")
        sock.connect(("8.8.8.8", 80))
        ip = sock.getsockname()[0]
    return ip

def new_get_system_info():
    try:
        info={}
        info['System']=platform.system()
        info['System-release']=platform.release()
        info['System-version']=platform.version()
        info['Architecture']=platform.machine()
        info['Processor']=platform.processor()
        info['Local IP'] = str(get_local_IP())
        if(info['System'] == "Linux"):
            info['Libc version'] = platform.libc_ver()[1]
        
        with open(SYS_INFO_PATH,'w') as sys_fd:
            json.dump(info,sys_fd,indent=2) # lưu vào file cho những lần sau
            logf.done(f"Đã lưu vào tệp tin {SYS_INFO_PATH}") # thông báo
        pJson(json.loads(json.dumps(info))) # in ra đẹp

    except Exception as e:
        logging.exception(e)    
    
    ''' some extend info '''
        # extend info
        # hostname = socket.gethostname()
        # info['Hostname']= hostname
        # info['Ip-address']=socket.gethostbyname(hostname)
        # info['Mac-address']=':'.join(re.findall('..', '%012x' % uuid.getnode()))

def get_system_info():
    if(check_exist_json_info_file()==1):
         return 1
    else:
        new_get_system_info()
