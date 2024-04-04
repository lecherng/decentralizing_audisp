#!/usr/bin/env python3

"""
parse audit events and sends them to syslog after changing uid to username
"""


"""
Todo
1. Check if we have the correct permission to run the audit.
2. syslog.closelog when terminated.
"""

__author__ = "Karim Boumedhel"                                                                                                                                 
__credits__ = ["Karim Boumedhel"]                                                                                                                              
__license__ = "GPL"                                                                                                                                            
__version__ = "1.0"
__maintainer__ = "Karim Boumedhel"
__email__ = "karimboumedhel@redhat.com"
__status__ = "Production"

import os
import signal
import sys
import auparse
import syslog
from io import StringIO

from threading import Thread
import time 

def dummyThreadA():
    i = 0
    while(True):
        i+=1
        print(i)
        if i > 40: break
        time.sleep(1)

def dummyThreadB():
    i = 0
    while(True):
        i+=1
        print(i)
        if i > 50: break
        time.sleep(1)

def main():
        threads = []
        t1 = Thread(target=dummyThreadA)
        t1.start()
        t2 = Thread(target=dummyThreadB)
        t2.start()
        threads.append(t1)
        threads.append(t2)

if  __name__ =='__main__':
        main()
