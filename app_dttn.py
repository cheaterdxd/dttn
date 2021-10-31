from menu_list import main_menu
import signal,sys
from linux.cve_2021_3156 import run_exploit
def signal_handler(signal, frame):
    print('\nBạn đã thoát chương trình bằng Ctrl+C. Hẹn gặp lại. ')
    sys.exit(0)



def main():
    signal.signal(signal.SIGINT, signal_handler)
    # main_menu()
    run_exploit.run()




if __name__ == "__main__":
    main()
