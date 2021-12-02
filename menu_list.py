'''
Các menu của chưƠng trình, xử lý nhận input và return input
'''


from formatOutput import prettyAnnounce as logf

from pathlib import Path
import importFile
from util import clean_terminal, stop_terminal

def cve_menu():
    clean_terminal()
    print(f'{logf.bcolors.WARNING}Danh sách cve hiện có{logf.bcolors.ENDC}')
    all_cve = []
    idx = 1
    for i in Path(importFile.root_directory + '/linux').iterdir():
        if(i.name.startswith('cve')):
            print(f"{logf.bcolors.OKCYAN}[{idx}] {logf.bcolors.ENDC}{i.name.upper()}")
            all_cve.append(i.name.upper()) # chuẩn format cho đẹp
            idx+=1
    print(f"{logf.bcolors.OKCYAN}[{0}] {logf.bcolors.ENDC}Thoát menu.")
    out_symbols = (f'\n{logf.bcolors.WARNING}(Chọn số) >>>{logf.bcolors.ENDC} ')
    while(1):
        try:
            cve_idx = int(input(out_symbols).strip('\n')) 
            if(cve_idx > len(all_cve)):
                logf.log.fail("CVE bạn chọn chưa được xây dựng! Hãy chọn một CVE trong danh sách.")
            elif(cve_idx == 0):
                break
            else:
                return str(all_cve[cve_idx-1]).lower() # lower_case
        except ValueError:
            logf.log.fail("Vui lòng chỉ nhập số trên lựa chọn!")
def menu_header(header:str,break_len):
    out_format_head = ''
    import textwrap
    out_format_head+=('┌'+'─'*(break_len+2)+'┐')+'\n'
    for i in header.split('\n'):
        te = textwrap.wrap(i,break_len,break_long_words=False)
        
        for line in te:
            align_len = int((break_len+2 - len(line))/2)
            align_text = align_len*' '+line+align_len*' '
            align_text = align_text.ljust(break_len+2,' ')
            out_format_head+=('│'+align_text+'│')+'\n'
    out_format_head+=('└'+'─'*(break_len+2)+'┘')+'\n'
    return out_format_head

def entry_dynamic_menu(options_text: list, number_of_ques:int, symbols_:str,quest_color='',symbols_color='',header=''):
    '''
    In ra một menu có form:
    Hãy chọn thao tác mong muốn

    1. options_text 1
    2. options_text 2
    ...
    0. Thoát

    symbols_  [Chờ nhập lựa chọn]

    Tham số:

    options_text    [List]: lựa chọn dướI dạng text
    number_of_ques  [int] : số dương lớn nhất của lựa chọn 
    symbols_        [str] : biểu tưỢng chờ nhập lựa chọn
    quest_color     [color]: màu của câu hỏi
    symbols_color   [color]: màu của symbols
    '''
    if(symbols_color!=''):        
        symbols_out = f'{symbols_color}{symbols_}{logf.bcolors.ENDC} '
    else:
        symbols_out = f'{logf.bcolors.OKCYAN}{symbols_}{logf.bcolors.ENDC} '
    
    while(1):
        clean_terminal()
        if(header!=''):
            print(menu_header(header,40))
        print(f"{logf.bcolors.WARNING}Hãy chọn thao tác mong muốn{logf.bcolors.ENDC}\n")
        idx = 1 # 0 là Thoát option
        for q_i in options_text:
            print(f"{idx}. {quest_color}{q_i}{logf.bcolors.ENDC}")
            idx+=1
        print("0. Thoát")
        print(end='\n')
        choice = str(input(symbols_out).strip('\n'))
        if(choice in ' '.join(str(i) for i in range(0,number_of_ques+1))):
            return (choice)
        else:
            print(end='\n')
            logf.log.fail("Lựa chọn không hợp lệ !\n")
            stop_terminal()
