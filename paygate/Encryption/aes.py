from argparse import *
from ..Encryption.readBlockFile import *
from ..Encryption.AES256 import encrypt, decrypt
import secrets
from ..Encryption.readKeyFile import *
import logging

logger = logging.getLogger(__name__)

keyfile = secrets.token_hex(32)


def encryptFile(filename):       
    plainBlock = getLargeBlock(filename)
    encryptedBlock = []
    lenFill = len(str(len(plainBlock)))

    # print("Plain text: ", filename)
    logger.warning("Plain text: ", filename)

    for i in range(len(plainBlock)):
        encryptedBlock.append(encrypt(plainBlock[i], getKey(keyfile)))
        # print("Encrypted: " + str(i).zfill(lenFill)+"/" + str(len(plainBlock)).zfill(lenFill)+"\r")  # check
        logger.warning("Encrypted: " + str(i).zfill(lenFill)+"/" + str(len(plainBlock)).zfill(lenFill)+"\r")
    # print("Encrypted: "+str(len(plainBlock)))
    logger.warning("Encrypted: "+str(len(plainBlock)))

    finaldata = writeToOutputHex(encryptedBlock)

    # print("Encrypted Data: ", finaldata)
    logger.warning("Encrypted Data: ", finaldata)

    return finaldata


def decryptFile(filename, keyfile1):
    inputBlock = getLargeHexBlock(filename)
    for i in range(len(inputBlock)):
        inputBlock[i] = decrypt(inputBlock[i], getKey(keyfile))
        # print("Decrypted: ", str(i).zfill(8)+"/"+str(len(inputBlock)).zfill(8)+"\r")  # check
        logger.warning("Decrypted: ", str(i).zfill(8)+"/"+str(len(inputBlock)).zfill(8)+"\r")

    finalDecryptdata = writeToOutputPlain(inputBlock)

    # print("Decrypted Data: ", finalDecryptdata)
    logger.warning("Decrypted Data: ", finalDecryptdata)

    return finalDecryptdata


def writeToOutputPlain(block):

    outputFile = ""

    lenFill = len(str(len(block)))
    k = 0
    while k < len(block):
        for j in range(0, len(block[k])):
            outputFile += chr(block[k][j])

        k += 1

    return outputFile


def writeToOutputHex(block):

    outputFile = ""
    k = 0
    lenFill = len(str(len(block)))
    while k < len(block):
        for j in range(0, len(block[k])):
            outputFile += (hex(block[k][j]))[2:].zfill(2)

        k += 1

    return outputFile


# def Main():

#     blockFile = input("Enter text to encrypt: ")

#     # This is a 256-bit hexxadecimal key
#     # generate this randomly
#     keyFile = "576E5A7234753778214125442A472D4B614E645267556B58703273357638792F"
#     enc_text = encryptFile(blockFile)
#     print("Encrypted data: ", enc_text)

#     dec_text = decryptFile(enc_text)
#     print("Decrypted data: ", dec_text)


# Main()