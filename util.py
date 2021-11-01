from posix import listdir
from pwnlib.util.proc import cwd
# from importFile import os
from pathlib import Path
import os
from formatOutput.prettyAnnounce import bcolors

def is_path_exist(path):
    return Path(path).exists()


# prefix components:
space =  '    '
branch = f'{bcolors.WARNING}│{bcolors.ENDC}   '
# pointers:
tee =    f'{bcolors.WARNING}├──{bcolors.ENDC} '
last =   f'{bcolors.WARNING}└──{bcolors.ENDC} '


def tree_in_verbose(dir_path: Path, prefix: str=''):
    """A recursive generator, given a directory Path object
    will yield a visual tree structure line by line
    with each line prefixed by the same characters
    """    
    contents = list(dir_path.iterdir())
    # contents each get pointers that are ├── with a final └── :
    pointers = [tee] * (len(contents) - 1) + [last]
    for pointer, path in zip(pointers, contents):
        if(path.is_dir()):
            yield prefix + pointer + bcolors.OKCYAN + path.name + bcolors.ENDC
            extension = branch if pointer == tee else space 
            # i.e. space because last, └── , above so no more |
            yield from tree_in_verbose(path, prefix=prefix+extension)
        else:
            yield prefix + pointer + path.name
        # if path.is_dir(): # extend the prefix and recurse:
            

def tree_dir(dir_path: Path, prefix: str=''):
    """A recursive generator, given a directory Path object
    will yield a visual tree structure line by line
    with each line prefixed by the same characters
    """    
    contents = list(dir_path.iterdir())
    # contents each get pointers that are ├── with a final └── :
    pointers = [tee] * (len(contents) - 1) + [last]
    for pointer, path in zip(pointers, contents):
        if(path.is_dir()):
            yield prefix + pointer + bcolors.OKCYAN + path.name + bcolors.ENDC
        else:
            yield prefix + pointer + path.name

def list_dir(path):
    # print(os.listdir(path))
    # for c in Path(path).iterdir():
    #     if(c.is_dir()==True):
    #         print(c.absolute())
    #         list_dir(c.absolute())
    for line in tree_dir(Path(path)):
        print(line)


def list_dir_verbose(path):
    for line in tree_in_verbose(Path(path)):
        print(line)


def main():
    # print(Path.home())
    # print_tree('/home/cheaterdxd/dttn')
    list_dir('/home/cheaterdxd')


if __name__ == "__main__":
    main()
