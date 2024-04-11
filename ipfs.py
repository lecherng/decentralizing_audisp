#!/usr/bin/env python3
import logging
import os
import requests
import json

logger = logging.getLogger(__name__)

class IPFS(object):
    def __init__(self, apiKeyFile):
        if apiKeyFile == None:
            logger.error(f"{apiKeyFile} variable is empty")
            raise ValueError ("no apiKeyFile is found")
        else:
            try:
                f = open(apiKeyFile, 'r')
                self.apiKey = f.read().replace("\n", "")
                f.close()
            except Exception as e:
                logger.error(f"{apiKeyFile} is not found")
                raise ValueError ("no apiKeyFile is found")

        self.ipfsRestApiUrl = "https://api.quicknode.com/ipfs/rest/v1/"
        self.ipfsUrl = "https://vessels-swam-except.quicknode-ipfs.com/ipfs/"
        self.restAPIHeaders = { 'x-api-key': self.apiKey }

    def add(self, filePath, fileType):
        """https://guides.quicknode.com/docs/ipfs/Pinning/upload-object"""
        addAPI = "s3/put-object"
        fileName = os.path.basename(filePath)

        url = self.ipfsRestApiUrl + addAPI
        payload = {'Key': fileName,
                   'ContentType': fileType}
        files=[('Body',(fileName, open(filePath,'rb'), fileType))]

        logger.debug(f"payload: {payload}")
        logger.debug(f"files: {files}")
        responseJson = json.loads(requests.request("POST", url, headers=self.restAPIHeaders, data=payload, files=files).text)
        logger.info(f"status: {responseJson['status']}, responseID: {responseJson['requestid']}, fileName: , {responseJson['pin']['name']}, contentID: {responseJson['pin']['cid']}")

        return responseJson['status'], responseJson['requestid'], responseJson['pin']['cid'], responseJson['pin']['name']

    def getUsingRequestID(self, requestID):
        """https://guides.quicknode.com/docs/ipfs/Pinning/get-object"""
        getAPI = f"s3/get-object/{requestID}"

        url = self.ipfsRestApiUrl + getAPI
        response = requests.request("GET", url, headers=self.restAPIHeaders, data={})
        logger.info(response.text)

    def getUsingCID(self, CID, fileName):
        url = f"{self.ipfsUrl}{CID}"
        fileName = url.split('/')[-1]
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(fileName, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8196):
                    f.write(chunk)

    def deleteUsingRequestID(self, requestID):
        """https://guides.quicknode.com/docs/ipfs/Pinning/delete-pinnedObject"""
        deleteAPI = f"pinning/{requestID}"

        url = self.ipfsRestApiUrl + deleteAPI
        response = requests.request("DELETE", url, headers=self.restAPIHeaders, data={})
        logger.info(response.text)

#from timeit import default_timer as timer

def main():
    logging.basicConfig(filename='logger.log', level=logging.INFO)

    ipfs = IPFS("apiKey")
    #start = timer()
    #status, resquestId, cid, name = ipfs.add("/home/yong/MyProject/decentralizing_ids/demofile_encrypted_0", "application/octet-stream")
    #end = timer()
    #logger.info(f"time: {end-start}")
    #if status == "pinned":
        #ipfs.getUsingRequestID(resquestId)
        #ipfs.deleteUsingRequestID(resquestId)
        #ipfs.getUsingCID(cid, name)

if  __name__ =='__main__':
        main()