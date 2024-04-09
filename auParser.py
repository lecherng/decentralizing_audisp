#!/usr/bin/env python3

import auparse
import re

class AuParser(object):
    def __init__(self, rbAuditEvent):
        self.rbAuditEvent = rbAuditEvent

    def auditParse(self, line):
        auParser = auparse.AuParser(auparse.AUSOURCE_BUFFER, line)
        auParser.reset()
        decodedProctitle = ''
        while True:
            if not auParser.first_record():
                raise ValueError (
                "AuParser is not the first record"
                )

            eventString = auParser.get_record_text()

            # handling the hex to string conversion in auditd log.
            if auParser.get_type_name() == "PROCTITLE":
                decodedProctitle = "proctitle=%s" % (bytes.fromhex(re.sub(r'00', "20", str(auParser.find_field("proctitle")))).decode('utf-8'))
                eventString = re.sub(r'proctitle=.*$', decodedProctitle, eventString)

            try:
                self.rbAuditEvent.enqueue("%s\n" % eventString)
            except Exception as e:
                print("unable to enqueue to ringbuffer: %s" % (e))
                break

            if not auParser.parse_next_event(): break