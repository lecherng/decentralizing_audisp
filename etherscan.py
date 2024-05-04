import logging
import requests
import json
import datetime
import calendar
from config import Config
from collections import namedtuple

logger = logging.getLogger(__name__)

class Etherscan(object):
    def __init__(self, config):
        self._etherscanKey = config.etherScanApiKey
        self._etherscanUrl = "https://api-sepolia.etherscan.io"
        self._smartContractAddr = config.smartContractAddr
        self._metaBlockchain = namedtuple('metaBlockchain', 'methodId ')
        return

    def __requestsApi(self, apiCmd):
        res = requests.get(apiCmd)
        if (res.status_code != 200):
            return None
        return res.text

    def __getBlockMinedFromTimestamp(self, timestamp, closest):
        getBlockMinedApi = f"/api?module=block&action=getblocknobytime&timestamp={timestamp}&closest={closest}&apikey={self._etherscanKey}"
        responseJson = json.loads(self.__requestsApi(f"{self._etherscanUrl}{getBlockMinedApi}"))
        if responseJson['status'] == "1":
            return responseJson['result']
        else:
            return None

    def getCIDFromRangeOfTime(self, fromTimeInDatetime, toTimeInDatetime):
        fromEpochTime = calendar.timegm(fromTimeInDatetime.timetuple())
        toEpochTime = calendar.timegm(toTimeInDatetime.timetuple())

        startBlock = self.__getBlockMinedFromTimestamp(fromEpochTime, "after")
        endBlock = self.__getBlockMinedFromTimestamp(toEpochTime, "before")

        return self.getCIDFromBlockRange(startBlock, endBlock)

    def getCIDFromBlockRange(self, startBlock = 0, endBlock = 99999999):
        getRangeTransactionApi = f"/api?module=account&action=txlist&address={self._smartContractAddr}&startblock={startBlock}&endblock={endBlock}&page=1&offset=10&sort=asc&apikey={self._etherscanKey}"
        responseJson = json.loads(self.__requestsApi(f"{self._etherscanUrl}{getRangeTransactionApi}"))
        listOfTransactionInput = []
        for item in responseJson['result']:
            if item['methodId'] == "0xdfb29935" and item['isError'] == "0":
                listOfTransactionInput.append(
                    item['input']
                    )
        logger.info(listOfTransactionInput)
        return listOfTransactionInput

from ethereum import Ethereum
from ipfs import IPFS
from util import Util

def main():
    logging.basicConfig(filename='logger.log', level=logging.INFO)
    config = Config()

    ipfsHandler = IPFS(config.apiKey)
    ethereumHandler = Ethereum(config.ethPrivKey, config.accountAddr, config.smartContractAddr, config.apiFile, config.urlProvider)
    etherscanHandler = Etherscan(config)
    util = Util(config)

    startTime = datetime.datetime(2024, 5, 1, 0, 0, 0)
    endTime = datetime.datetime(2024, 5, 5, 0, 0, 0)

    listOfTransactionInput = etherscanHandler.getCIDFromRangeOfTime(startTime, endTime)

    for item in listOfTransactionInput:
        cid = ethereumHandler.getCIDFromTransactionInput(item)
        logger.info(cid)
        ipfsHandler.getFileUsingCID(cid, item)
        util.decryptLogFile(cid)
    return

if  __name__ =='__main__':
    main()