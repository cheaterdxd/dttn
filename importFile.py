import platform
import socket
import json
import logging
import sys, os
import subprocess 
import shlex
from pwn import *

global root_directory, os_type
root_directory = os.path.dirname(__file__)
os_type = ""

