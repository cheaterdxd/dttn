from importFile import subprocess as subpr
from importFile import shlex


def executeOnce(command):
    '''
        Thực thi lệnh 1 lần và lấy trả về của lệnh
        args: command in one line
        return: output of command
    '''

    args_l = shlex.split(command)
    # print(command)
    return subpr.run(args_l,stdout=subpr.PIPE, stderr=subpr.PIPE)

def executeInteractive(command):
    '''Thực thi lệnh và nói chuyện với tiến trình mới'''
    args_l = shlex.split(command)
    return subpr.Popen(args_l,stdout=subpr.PIPE)