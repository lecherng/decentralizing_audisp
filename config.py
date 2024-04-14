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
        self.ethPrivKeyFile = config['Filename']['EthPrivKey']

        self.audispBufferSize = int(config['Buffer']['AudispBuffer'])
        self.maxAuditEvent = int(config['Buffer']['MaxAuditEvent'])

        self.smartContractAddr = config['Ethereum']['SmartContractAddress']
        self.accountAddr = config['Ethereum']['AccountAddress']
        self.apiFile = config['Ethereum']['AbiFile']
        self.urlProvider = config['Ethereum']['UrlProvider']

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

    def getEthPrivKey(self):
        ethPrivKey = None
        try:
            f = open(self.ethPrivKeyFile, 'r')
            ethPrivKey = f.read().replace("\n", "")
            f.close()
        except Exception as _:
            logger.error(f"{self.ethPrivKeyFile} is not found")
            raise ValueError ("no ethPrivKeyFile is found")
        return ethPrivKey

    def getAudispBufferSize(self):
        return self.audispBufferSize

    def getMaxAuditEvent(self):
        return self.maxAuditEvent

    def getSmartContractAddr(self):
        return self.smartContractAddr

    def getAccountAddr(self):
        return self.accountAddr

    def getAbi(self):
        abi = None
        try:
            f = open(self.apiFile, 'r')
            abi = f.read()
            f.close()
        except Exception as _:
            logger.error(f"{self.apiFile} is not found")
            raise ValueError ("no apiFile is found")
        return abi

    def getUrlProvider(self):
        return self.urlProvider