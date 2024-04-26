#!/usr/bin/env python3
import logging
import os
import requests
import json
import hashlib
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class IpfsMetadata:
    #status: str
    #requestID: str
    fileName: str
    contentID: str
    fileSize: int
    timestamp: str

    def getHashOfMetadata(self):
        return hashlib.sha256(str(self).encode('utf-8')).hexdigest()

class IPFS(object):
    def __init__(self, apiKey):
        self._apiKey = apiKey
        self._ipfsRestApiUrl = "https://api.quicknode.com/ipfs/rest/v1/"
        self._ipfsUrl = "https://vessels-swam-except.quicknode-ipfs.com/ipfs/"
        self._restAPIHeaders = { 'x-api-key': self._apiKey }

    def add(self, filePath, fileType) -> IpfsMetadata:
        """https://guides.quicknode.com/docs/ipfs/Pinning/upload-object"""
        addAPI = "s3/put-object"
        fileName = os.path.basename(filePath)

        url = self._ipfsRestApiUrl + addAPI
        payload = {'Key': fileName,
                   'ContentType': fileType}
        files=[('Body',(fileName, open(filePath,'rb'), fileType))]

        logger.debug(f"payload: {payload}")
        logger.debug(f"files: {files}")
        responseJson = json.loads(requests.request("POST", url, headers=self._restAPIHeaders, data=payload, files=files).text)

        #return IpfsMetadata(responseJson['status'], responseJson['requestid'], responseJson['pin']['name'], responseJson['pin']['cid'], int(responseJson['info']['size']), responseJson['created'])
        return IpfsMetadata(responseJson['pin']['name'], responseJson['pin']['cid'], int(responseJson['info']['size']), responseJson['created'])


    def getUsingRequestID(self, requestID) -> None:
        """https://guides.quicknode.com/docs/ipfs/Pinning/get-object"""
        getAPI = f"s3/get-object/{requestID}"

        url = self._ipfsRestApiUrl + getAPI
        response = requests.request("GET", url, headers=self._restAPIHeaders, data={})
        logger.info(response.text)

    def getFileUsingCID(self, CID, fileName) -> None:
        url = f"{self._ipfsUrl}{CID}"
        fileName = url.split('/')[-1]
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(fileName, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8196):
                    f.write(chunk)

    def deleteUsingRequestID(self, requestID) -> None:
        """https://guides.quicknode.com/docs/ipfs/Pinning/delete-pinnedObject"""
        deleteAPI = f"pinning/{requestID}"

        url = self._ipfsRestApiUrl + deleteAPI
        response = requests.request("DELETE", url, headers=self._restAPIHeaders, data={})
        logger.info(response.text)

    def getPinnedFile(self) -> list:
        """https://www.quicknode.com/docs/ipfs/Pinning/get-all-pinnedObjects"""
        pinnedFileApi = "pinning?pageNumber=1&perPage=10"
        listOfFile = []

        url = self._ipfsRestApiUrl + pinnedFileApi
        #response = requests.request("GET", url, headers=self.restAPIHeaders, data={})
        responseJson = json.loads(requests.request("GET", url, headers=self._restAPIHeaders, data={}).text)

        for item in responseJson['data']:
            listOfFile.append(
                #IpfsMetadata(item['status'], item['requestId'], item['name'], item['cid'], int(item['size']), item['updatedAt'])
                IpfsMetadata(item['name'], item['cid'], int(item['size']), item['updatedAt'])
                )
        logger.info(listOfFile)

        return listOfFile

from timeit import default_timer as timer
from config import Config

def main():
    logging.basicConfig(filename='logger.log', level=logging.INFO)
    config = Config()

    #ipfs = IPFS(config.apiKey)
    #start = timer()
    #ipfsMetadata = ipfs.add("/home/yong/MyProject/decentralizing_audisp/demofile_encrypted_0", "application/octet-stream")
    #end = timer()
    #logger.info(f"time: {end-start}")
    #if ipfsMetadata.status == "pinned":
        #ipfs.getUsingRequestID(resquestId)
        #ipfs.deleteUsingRequestID(resquestId)
        #ipfs.getFileUsingCID(cid, name)
    #    ipfs.getPinnedFile()

if  __name__ =='__main__':
    main()