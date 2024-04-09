#!/usr/bin/env python3

from ecies.utils import generate_key
from ecies import encrypt, decrypt

class Util(object):

    def __init__(self, filename, secretKey=None):
        self.filename = filename
        self.filenameEncrypted = "%s_encrypted" % (filename)
        self.index = 0
        if secretKey == None:
            self.secretKey = generate_key()
        else:
            self.secretKey = secretKey

        self.sk_bytes = self.secretKey.secret
        self.pk_bytes = self.secretKey.public_key.format(True)


    def writeToLogFile(self, buffer, index):
        try:
            f = open("%s_%d" % (self.filenameEncrypted, index), 'wb')
            f.write(buffer)
            f.close()
            self.index += 1
        except IOError as e:
            print(e)
            f.close()

    def readFromLogFile(self, index):
        buf = ""
        try:
            f = open("%s_%d" % (self.filenameEncrypted, index), 'rb')
            buf = f.read()
        except IOError as e:
            print(e)
            f.close()
        return buf

    def encryptLogFile(self, buf):
            encrypted = encrypt(self.pk_bytes, buf)
            currentIndex = self.index
            self.filename = "%s_%d" % (self.filenameEncrypted, currentIndex)
            try:
                self.writeToLogFile(encrypted, currentIndex)
            except IOError as e:
                print(e)
                return

            print("%d: %s" % (currentIndex, decrypt(self.sk_bytes, self.readFromLogFile(currentIndex))))