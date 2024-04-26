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
        self.privKey = privKey
        self.accountAddr = accountAddr
        self.smartContractAddr = smartContractAddr
        self.contract = None
        self.abi = abi

        self.web3 = Web3(Web3.HTTPProvider(urlProvider))

        self.isConnected = self.web3.is_connected()

        if self.isConnected:
            self.contract = self.web3.eth.contract(address = self.smartContractAddr, abi = self.abi)

    def getMetadataFromBlockchain(self):
        result = None
        if self.isConnected:
            result = self.contract.functions.getHash().call()
            logger.info(f"getHash {result}")
        return result

    def addMetadataToBlockchain(self, metadata):
        if not self.isConnected:
            return None

        account = self.web3.eth.account.from_key(self.privKey)
        unsignedTxn = self.contract.functions.sendHash(metadata).build_transaction({
            'from': account.address,
            'nonce': self.web3.eth.get_transaction_count(account.address),
        })
        signedTxn = self.web3.eth.account.sign_transaction(unsignedTxn, private_key = account.key)
        start = timer()
        txHash = self.web3.eth.send_raw_transaction(signedTxn.rawTransaction)
        self.web3.eth.wait_for_transaction_receipt(txHash)
        end = timer()
        logger.info(f"time: {end-start}")
        logger.info(f"txHash: {binascii.hexlify(txHash)}")
        return txHash

    def getTransactionByHash(self, txHash):
        if not self.isConnected:
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