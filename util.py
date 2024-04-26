#!/usr/bin/env python3
from ecies.utils import generate_key
from ecies import encrypt, decrypt
import logging
import binascii
import struct
from ipfs import IpfsMetadata, IPFS
from config import Config
from ethereum import Ethereum

logger = logging.getLogger(__name__)

class Util(object):
    def __init__(self, config):
        self.ipfsHandler = IPFS(config.apiKey)
        self.ethereumHandler = Ethereum(config.ethPrivKey, config.accountAddr, config.smartContractAddr, config.apiFile, config.urlProvider)
        self.filename = config.filename
        self.filenameEncrypted = "%s_encrypted" % (self.filename)
        self.index = 0
        self.previousBlockchainHashTx = b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
        if config.privKey == None:
            self.sk_bytes = generate_key().secret
        else:
            self.sk_bytes = config.privKey

        if config.pubKey == None:
            self.pk_bytes = self.sk_bytes.public_key.format(False)
        else:
            self.pk_bytes = config.pubKey

        #logger.debug(f'pubKey {binascii.hexlify(self.pk_bytes)}')
        #logger.debug(f'privKey {binascii.hexlify(self.sk_bytes)}')

    def __writeToLogFile(self, buffer, index):
        try:
            with open("%s_%d" % (self.filenameEncrypted, index), 'wb') as f:
                f.write(buffer)
            self.index += 1
        except IOError as e:
            logger.error("IOError: %s" % (e))

    def __uploadToIPFS(self, index):
        return self.ipfsHandler.add("%s_%d" % (self.filenameEncrypted, index), "application/octet-stream")

    def __uploadToBlockchain(self, ipfsMetadata):
        self.previousBlockchainHashTx = self.ethereumHandler.addMetadataToBlockchain(ipfsMetadata.contentID)
        return None

    def readFromLogFile(self, index):
        buf = ""
        try:
            with open("%s_%d" % (self.filenameEncrypted, index), 'rb') as f:
                buf = f.read()
        except IOError as e:
            logger.error("IOError: %s" % (e))
        return buf

    def encryptLogFile(self, buf):
            currentIndex = self.index

            # | block index (8Bytes) | previous hashTx (32Bytes) | ciphertext |
            encrypted = bytearray()
            encrypted.extend(struct.pack('>Q', currentIndex))
            encrypted.extend(self.previousBlockchainHashTx)
            encrypted.extend(encrypt(self.pk_bytes, buf))

            self.filename = "%s_%d" % (self.filenameEncrypted, currentIndex)
            try:
                self.__writeToLogFile(encrypted, currentIndex)
                ipfsMetadata = self.__uploadToIPFS(currentIndex)
                self.__uploadToBlockchain(ipfsMetadata)
            except IOError as e:
                logger.error("IOError: %s" % (e))
                return

            #logger.debug("Decrypted: %s" % (decrypt(self.sk_bytes, self.readFromLogFile(currentIndex))))
