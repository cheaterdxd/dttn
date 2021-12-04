import platform
import socket
import json
import logging
import sys, os
import subprocess 
import shlex
import signal
from pwn import *

global root_directory, os_type
root_directory = os.path.dirname(__file__)
os_type = ""
is_exist_bug = -1
