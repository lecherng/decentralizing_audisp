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
        self._ipfsHandler = IPFS(config.apiKey)
        self._ethereumHandler = Ethereum(config.ethPrivKey, config.accountAddr, config.smartContractAddr, config.apiFile, config.urlProvider)
        self._filename = config.filename
        self._filenameEncrypted = "%s_encrypted" % (self._filename)
        self._index = 0
        self._previousBlockchainHashTx = b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
        if config.privKey == None:
            self._skBytes = generate_key().secret
        else:
            self._skBytes = config.privKey

        if config.pubKey == None:
            self._pkBytes = self._skBytes.public_key.format(False)
        else:
            self._pkBytes = config.pubKey

        #logger.debug(f'pubKey {binascii.hexlify(self.pk_bytes)}')
        #logger.debug(f'privKey {binascii.hexlify(self.sk_bytes)}')

    def __writeToLogFile(self, buffer, index):
        try:
            with open("%s_%d" % (self._filenameEncrypted, index), 'wb') as f:
                f.write(buffer)
            self._index += 1
        except IOError as e:
            logger.error("IOError: %s" % (e))

    def __uploadToIPFS(self, index):
        return self._ipfsHandler.add("%s_%d" % (self._filenameEncrypted, index), "application/octet-stream")

    def __uploadToBlockchain(self, ipfsMetadata):
        self._previousBlockchainHashTx = self._ethereumHandler.addMetadataToBlockchain(ipfsMetadata.contentID)
        return None

    def readFromLogFile(self, index):
        buf = ""
        try:
            with open("%s_%d" % (self._filenameEncrypted, index), 'rb') as f:
                buf = f.read()
        except IOError as e:
            logger.error("IOError: %s" % (e))
        return buf

    def encryptLogFile(self, buf):
            currentIndex = self._index

            # | block index (8Bytes) | previous hashTx (32Bytes) | ciphertext |
            encrypted = bytearray()
            encrypted.extend(struct.pack('>Q', currentIndex))
            encrypted.extend(self._previousBlockchainHashTx)
            encrypted.extend(encrypt(self._pkBytes, buf))

            self._filename = "%s_%d" % (self._filenameEncrypted, currentIndex)
            try:
                self.__writeToLogFile(encrypted, currentIndex)
                ipfsMetadata = self.__uploadToIPFS(currentIndex)
                self.__uploadToBlockchain(ipfsMetadata)
            except IOError as e:
                logger.error("IOError: %s" % (e))
                return

            #logger.debug("Decrypted: %s" % (decrypt(self.sk_bytes, self.readFromLogFile(currentIndex))))
