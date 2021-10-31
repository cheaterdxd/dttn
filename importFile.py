import platform
import socket
import json
import logging
import sys, os
import subprocess 
import shlex
from pwn import *

root_directory = os.path.dirname(__file__)

