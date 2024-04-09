#!/usr/bin/env python3

"""
parse audit events and sends them to syslog after changing uid to username
"""


"""
Todo
1. Check if we have the correct permission to run the audit.
2. syslog.closelog when terminated.
"""

__author__ = ""                                                                                                                                 
__credits__ = [""]                                                                                                                              
__license__ = "GPL"                                                                                                                                            
__version__ = "1.0"
__maintainer__ = ""
__email__ = ""
__status__ = ""

import os
import signal
import sys
from circularBuffer import StringCircularBuffer
from util import Util
from auParser import AuParser
from threading import Thread
import logging

logger = logging.getLogger(__name__)

stop = 0
hup = 0
debug = 0

def termHandler(signum, _):
    global stop 
    signame = signal.Signals(signum).name
    logger.info(f'Signal handler called with signal {signame} ({signum})')
    stop = 1

def hupHandler(signum, _):
    global hup
    signame = signal.Signals(signum).name
    logger.info(f'Signal handler called with signal {signame} ({signum})')
    hup = 1

def reloadConfig():
    global hup
    hup = 0

signal.signal(signal.SIGHUP, hupHandler)
signal.signal(signal.SIGTERM, termHandler)
signal.signal(signal.SIGINT, termHandler)
        
def auditDispatcherThread(rbAuditEvent):
    global stop
    global hup
    auparser = AuParser(rbAuditEvent)

    while stop == 0:
        try:
            if debug == 1:
                f = open("test.log", "r")
                buf = f.readlines()
            else:
                #buf=sys.stdin.readlines() # for testing
                buf=sys.stdin            # for actual

            if hup == 1 :
                reloadConfig()
                continue
            for line in buf:
                #logger.info(line)
                auparser.auditParse(line)
        except IOError as e:
            logger.error("IOError: %s" % (e))
            continue
        except ValueError as e:
            logger.error("ValueError %s" % (e))
        if debug == 1: stop = 1

def auditLoggerThread(filename, rbAuditEvent):
    global stop
    global hup

    util = Util(filename)

    # ringBuffer for 512 Security Events
    rbLogger = StringCircularBuffer(6144)
    while True:
        try:
            if not rbAuditEvent.is_empty() and not rbLogger.is_full():
                rbLogger.enqueue(rbAuditEvent.dequeue())

            if rbLogger.is_full():
                util.encryptLogFile(rbLogger.flush_content())
                continue
            #get the last piece of data out from the ring buffer.
            elif not rbAuditEvent.is_empty():
                continue
            elif stop:
                util.encryptLogFile(rbLogger.flush_content())
                break
        except Exception as e:
            logger.error("unable to enqueue/dequeue to ringbuffer: %s" % (e))
            break

def main():
    rbAuditEvent = StringCircularBuffer(16392)
    logging.basicConfig(filename='logger.log', level=logging.INFO)
    filename = "demofile"

    logger.info("Start")
    

    threads = []
    t1 = Thread(target=auditDispatcherThread, args=(rbAuditEvent,))
    t2 = Thread(target=auditLoggerThread, args=(filename, rbAuditEvent,))
    t1.start()
    t2.start()
    threads.append(t1)
    threads.append(t2)
    
    t1.join()
    t2.join()

if  __name__ =='__main__':
        main()
