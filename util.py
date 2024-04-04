#!/usr/bin/env python3

from ecies.utils import generate_key
from ecies import encrypt, decrypt

class Util(object):

    def __init__(self, filename, secretKey=None):
        self.filename = filename
        self.index = 0
        if secretKey == None:
            self.secretKey = generate_key()
        else:
            self.secretKey = secretKey

        self.sk_bytes = self.secretKey.secret
        self.pk_bytes = self.secretKey.public_key.format(True)


    def writeToLogFile(self, buffer):
        try:
            f = open(self.filename, 'wb')
            f.write(buffer)
            f.close()
            self.index += 1
        except IOError as e:
            print(e)
            f.close()

    def readFromLogFile(self):
        buf = ""
        try:
            f = open(self.filename, 'rb')
            buf = f.read()
        except IOError as e:
            print(e)
            f.close()
        return buf

    def encryptLogFile(self, buf):
            encrypted = encrypt(self.pk_bytes, buf)

            self.filename = "%s_%d.encrypted" % (self.filename, self.index)
            try:
                self.writeToLogFile(encrypted)
            except IOError as e:
                return

            print(decrypt(self.sk_bytes, self.readFromLogFile()))