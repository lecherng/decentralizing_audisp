import logging
import configparser

logger = logging.getLogger(__name__)

class Config(object):
    def __init__(self):
        self.configFile = "decentralized_audisp.conf"

        config = configparser.ConfigParser()
        config.read(self.configFile)

        self.pubKeyFile = config['Filename']['PubKeyFile']
        self.privKeyFile = config['Filename']['PrivKeyFile']
        self.apiKeyFile = config['Filename']['IPFSApiKeyFile']
        self.filename = config['Filename']['EncryptedIDSFile']
        self.loggerFilename = config['Filename']['LoggerFile']

        self.audispBufferSize = int(config['Buffer']['AudispBuffer'])
        self.maxAuditEvent = int(config['Buffer']['MaxAuditEvent'])

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

    def getAudispBufferSize(self):
        return self.audispBufferSize

    def getMaxAuditEvent(self):
        return self.maxAuditEvent