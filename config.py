import logging
import configparser

logger = logging.getLogger(__name__)

class Config(object):
    def __init__(self):
        self._configFile = "decentralized_audisp.conf"

        config = configparser.ConfigParser()
        config.read(self._configFile)

        self._pubKey = self.__readFromFile(config['Filename']['PubKeyFile'], 'rb')
        self._privKey = self.__readFromFile(config['Filename']['PrivKeyFile'], 'rb')
        self._apiKey = self.__readFromFile(config['Filename']['IPFSApiKeyFile'], 'r', True)
        self._filename = config['Filename']['EncryptedIDSFile']
        self._loggerFilename = config['Filename']['LoggerFile']
        self._ethPrivKey = self.__readFromFile(config['Filename']['EthPrivKey'], 'r', True)

        self._audispBufferSize = int(config['Buffer']['AudispBuffer'])
        self._maxAuditEvent = int(config['Buffer']['MaxAuditEvent'])

        self._smartContractAddr = config['Ethereum']['SmartContractAddress']
        self._accountAddr = config['Ethereum']['AccountAddress']
        self._apiFile = self.__readFromFile(config['Ethereum']['AbiFile'], 'r')
        self._urlProvider = config['Ethereum']['UrlProvider']

        self._etherScanApiKey = self.__readFromFile(config['Etherscan']['ApiKey'], 'r')

    def __readFromFile(self, path, mode, isRemoveNewLine = False):
        buffer = None
        try:
            with open(path, mode) as f:
                buffer = f.read()
                if isRemoveNewLine: 
                    buffer = buffer.replace("\n", "")
        except Exception as _:
            logger.error(f"{path} is not found")
            raise ValueError (f"no {path} is found")
        return buffer

    @property
    def pubKey(self):
        return self._pubKey
    
    @property
    def privKey(self):
        return self._privKey
    
    @property
    def apiKey(self):
        return self._apiKey
    
    @property
    def filename(self):
        return self._filename
    
    @property
    def loggerFilename(self):
        return self._loggerFilename
    
    @property
    def ethPrivKey(self):
        return self._ethPrivKey
    
    @property
    def audispBufferSize(self):
        return self._audispBufferSize
    
    @property
    def maxAuditEvent(self):
        return self._maxAuditEvent
    
    @property
    def smartContractAddr(self):
        return self._smartContractAddr
    
    @property
    def accountAddr(self):
        return self._accountAddr
    
    @property
    def apiFile(self):
        return self._apiFile
    
    @property
    def urlProvider(self):
        return self._urlProvider

    @property
    def etherScanApiKey(self):
        return self._etherScanApiKey