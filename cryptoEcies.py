#!/usr/bin/env python3

"""
encrypt with ecies.
"""

__author__ = "Karim Boumedhel"                                                                                                                                 
__credits__ = ["Karim Boumedhel"]                                                                                                                              
__license__ = "GPL"                                                                                                                                            
__version__ = "1.0"
__maintainer__ = "Karim Boumedhel"
__email__ = "karimboumedhel@redhat.com"
__status__ = "Production"

from ecies.utils import generate_key
from ecies import encrypt, decrypt

def main():
        secp_k = generate_key()
        sk_bytes = secp_k.secret
        pk_bytes = secp_k.public_key.format(True)

        print(sk_bytes)
        print(pk_bytes)

        data = b'this is a test'

        print(decrypt(sk_bytes, encrypt(pk_bytes, data)))

if  __name__ =='__main__':
        main()
