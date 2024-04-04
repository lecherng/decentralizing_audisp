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
import auparse
import re
from circularBuffer import StringCircularBuffer
from threading import Thread

from ecies.utils import generate_key
from ecies import encrypt, decrypt


stop = 0
hup = 0

def termHandler(sig, msg):
    global stop 
    print("received a %d event, message: %d", sig, msg)
    stop = 1
    sys.exit(0)

def hupHandler(sig, msg):
    global hup
    print("received a %d event, message: %s", sig, msg)
    hup = 1

def reloadConfig():
    global hup
    hup = 0

signal.signal(signal.SIGHUP, hupHandler)
signal.signal(signal.SIGTERM, termHandler)

#buf=sys.stdin.readlines()
programname = os.path.basename(sys.argv[0])

def auditParse(auParser, rbAuditEvent):
    auParser.reset()
    decodedProctitle = ''
    while True:
        if not auParser.first_record():
            sys.exit(1)

        eventString = auParser.get_record_text()
        
        # handling the hex to string conversion in auditd log.
        if auParser.get_type_name() == "PROCTITLE":
            decodedProctitle = "proctitle=%s" % (bytes.fromhex(re.sub(r'00', "20", str(auParser.find_field("proctitle")))).decode('utf-8'))
            eventString = re.sub(r'proctitle=.*$', decodedProctitle, eventString)
        buf = "%s\n" % eventString
        rbAuditEvent.enqueue("%s\n" % eventString)

        if not auParser.parse_next_event(): break
        
def auditDispatcherThread(rbAuditEvent):
    global stop
    global hup

    while stop == 0:
        try:
            #buf=sys.stdin.readlines()
            #buf=sys.stdin
            f = open("test.log", "r")
            if hup == 1 :
                reloadConfig()
                continue
            for line in f.readlines():
                auParser = auparse.AuParser(auparse.AUSOURCE_BUFFER, line)
                auditParse(auParser, rbAuditEvent)
            #print(str(rb))
        except IOError as e:
            print(e)
            continue
        stop = 1

def writeToLogFile(filename, buffer):
    try:  
        f = open(filename, "a")
        f.write(buffer)
        f.close()      
    except IOError as e:
        print(e)
        f.close()

def encryptLogFile(filename, buf):
        secp_k = generate_key()
        sk_bytes = secp_k.secret
        pk_bytes = secp_k.public_key.format(True)
        
        #print(sk_bytes)
        #print(pk_bytes)

        #f = open(filename, 'r')
        #print(f.read().encode("utf-8"))

        #print()
        f1 = open("%s_encrypted" % (filename), 'wb')
        encrypted = encrypt(pk_bytes, buf)
        f1.write(encrypted)
        f1.close()

        f2 = open("%s_encrypted" % (filename), 'rb')
        encrypted2 = f2.read()
        
        print(decrypt(sk_bytes, encrypted2))

def auditLoggerThread(filename, rbAuditEvent):
    global stop
    global hup

    indexLogFile = 0

              
    # ringBuffer for 512Kb
    rbLogger = StringCircularBuffer(4)
    while True:
        if not rbAuditEvent.is_empty() and not rbLogger.is_full():
            rbLogger.enqueue(rbAuditEvent.dequeue())

        if rbLogger.is_full():
            #while not rbLogger.is_empty():
            #    writeToLogFile("%s_%d.txt" % (filename, indexLogFile), rbLogger.dequeue())
            encryptLogFile("%s_%d.txt" % (filename, indexLogFile), rbLogger.flush_content())
            indexLogFile += 1
            continue
        #get the last piece of data out from the ring buffer.
        elif not rbAuditEvent.is_empty():
            continue
        elif stop:
            #while not rbLogger.is_empty():
            #    writeToLogFile("%s_%d.txt" % (filename, indexLogFile), rbLogger.dequeue())
            encryptLogFile("%s_%d.txt" % (filename, indexLogFile), rbLogger.flush_content())
            indexLogFile += 1
            break

def main():
    rbAuditEvent = StringCircularBuffer(16384)
    filename = "demofile"

    threads = []
    t1 = Thread(target=auditDispatcherThread, args=(rbAuditEvent,))
    t2 = Thread(target=auditLoggerThread, args=(filename, rbAuditEvent,))
    t1.start()
    t2.start()
    threads.append(t1)
    threads.append(t2)
    
    while stop == 0:
          if stop == 1:
                break
    
    t1.join()
    t2.join()


if  __name__ =='__main__':
        main()
