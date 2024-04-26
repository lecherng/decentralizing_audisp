#!/usr/bin/env python3
import logging
import binascii
from web3 import Web3, eth
from timeit import default_timer as timer

logger = logging.getLogger(__name__)

"""
Metadata:
CID:
Hash of IPFS metadata:
"""

class Ethereum(object):
    def __init__(self, privKey, accountAddr, smartContractAddr, abi, urlProvider):
        self._privKey = privKey
        self._accountAddr = accountAddr
        self._smartContractAddr = smartContractAddr
        self._contract = None
        self._abi = abi
        self._web3 = Web3(Web3.HTTPProvider(urlProvider))
        self._isConnected = self._web3.is_connected()

        if self._isConnected:
            self._contract = self._web3.eth.contract(address = self._smartContractAddr, abi = self._abi)

    def getMetadataFromSmartContract(self):
        result = None
        if self._isConnected:
            result = self._contract.functions.getHash().call()
            logger.info(f"getHash {result}")
        return result

    def addMetadataToBlockchain(self, metadata):
        if not self._isConnected:
            return None

        account = self._web3.eth.account.from_key(self._privKey)
        unsignedTxn = self._contract.functions.sendHash(metadata).build_transaction({
            'from': account.address,
            'nonce': self._web3.eth.get_transaction_count(account.address),
        })
        signedTxn = self._web3.eth.account.sign_transaction(unsignedTxn, private_key = account.key)
        start = timer()
        txHash = self._web3.eth.send_raw_transaction(signedTxn.rawTransaction)
        self._web3.eth.wait_for_transaction_receipt(txHash)
        end = timer()
        logger.info(f"time: {end-start}")
        logger.info(f"txHash: {binascii.hexlify(txHash)}")
        return txHash

    def getTransactionByHash(self, txHash):
        if not self._isConnected:
            return None
        return eth.Eth.get_transaction(txHash)

from config import Config

def main():
    logging.basicConfig(filename='logger.log', level=logging.INFO)

    config = Config()
    test = Ethereum(config.ethPrivKey, config.accountAddr, config.smartContractAddr, config.apiFile, config.urlProvider)
    #test.getMetadataFromBlockchain()
    #test.addMetadataToBlockchain("QmcWEEXFxBERHiEYYA9yXgzbA9TTJ61N66GKFJ1ssmec97")
    #test.getMetadataFromBlockchain()

if  __name__ =='__main__':
    main()