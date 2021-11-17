
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

type_of_log = {
    'done': [bcolors.OKGREEN,'v'],
    'fail': [bcolors.FAIL,'-'],
    'info': [bcolors.OKBLUE,'*'],
    'warning': [bcolors.WARNING, '!']
}

# def print_error_bo
class log:
    def done(mess):
        log.print_it_out(type_of_log[log.done.__name__][0],type_of_log[log.done.__name__][1],mess)
    def fail(mess):
        log.print_it_out(type_of_log[log.fail.__name__][0],type_of_log[log.fail.__name__][1],mess)
    def info(mess):
        log.print_it_out(type_of_log[log.info.__name__][0],type_of_log[log.info.__name__][1],mess)
    def warning(mess):
        log.print_it_out(type_of_log[log.warning.__name__][0],type_of_log[log.warning.__name__][1],mess)

    def print_it_out(color, symbols, mess, endc='\n'):
        print(f"{color}[{symbols}] {bcolors.ENDC} {mess}",end=endc)
