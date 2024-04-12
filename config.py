import logging

logger = logging.getLogger(__name__)

class Config(object):
    def __init__(self):
        self.pubKeyFile = "pubKey"
        self.privKeyFile = "privKey"
        self.apiKeyFile = "apiKey"
        self.filename = "demofile"
        self.loggerFilename = "logger.log"

    def getPubKey(self):
        pubKey = None
        try:
            f = open(self.pubKeyFile, 'rb')
            pubKey = f.read()
            f.close()
        except Exception as _:
            logger.error(f"{self.pubKeyFile} is not found")
            raise ValueError ("no pubKeyFile is found")
        return pubKey
    
    def getPrivKey(self):   
        privKey = None
        try:
            f = open(self.privKeyFile, 'rb')
            privKey = f.read()
            f.close()
        except Exception as _:
            logger.error(f"{self.privKeyFile} is not found")
            raise ValueError ("no privKeyFile is found")
        return privKey
    
    def getApiKey(self):  
        apiKey = None
        try:
            f = open(self.apiKeyFile, 'r')
            apiKey = f.read().replace("\n", "")
            f.close()
        except Exception as _:
            logger.error(f"{self.apiKeyFile} is not found")
            raise ValueError ("no apiKeyFile is found")
        return apiKey