#!/usr/bin/env python3
from ecies.utils import generate_key
from ecies import encrypt, decrypt
import logging
import binascii

logger = logging.getLogger(__name__)

class Util(object):

    def __init__(self, filename, pubKey=None, privKey=None):
        self.filename = filename
        self.filenameEncrypted = "%s_encrypted" % (filename)
        self.index = 0
        if privKey == None:
            self.sk_bytes = generate_key().secret
        else:
            self.sk_bytes = privKey

        if pubKey == None:
            self.pk_bytes = self.sk_bytes.public_key.format(False)
        else:
            self.pk_bytes = pubKey

        logger.debug(f'pubKey {binascii.hexlify(self.pk_bytes)}')
        logger.debug(f'privKey {binascii.hexlify(self.sk_bytes)}')

    def writeToLogFile(self, buffer, index):
        try:
            f = open("%s_%d" % (self.filenameEncrypted, index), 'wb')
            f.write(buffer)
            f.close()
            self.index += 1
        except IOError as e:
            logger.error("IOError: %s" % (e))
            f.close()

    def readFromLogFile(self, index):
        buf = ""
        try:
            f = open("%s_%d" % (self.filenameEncrypted, index), 'rb')
            buf = f.read()
        except IOError as e:
            logger.error("IOError: %s" % (e))
            f.close()
        return buf

    def encryptLogFile(self, buf):
            encrypted = encrypt(self.pk_bytes, buf)
            currentIndex = self.index
            self.filename = "%s_%d" % (self.filenameEncrypted, currentIndex)
            try:
                self.writeToLogFile(encrypted, currentIndex)
            except IOError as e:
                logger.error("IOError: %s" % (e))
                return

            logger.debug("Decrypted: %s" % (decrypt(self.sk_bytes, self.readFromLogFile(currentIndex))))
