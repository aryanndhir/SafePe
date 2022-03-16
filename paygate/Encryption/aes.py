from argparse import *
from ..Encryption.readBlockFile import *
from ..Encryption.AES256 import encrypt, decrypt
import secrets
from ..Encryption.readKeyFile import *


keyfile = secrets.token_hex(32)
print(keyfile)


def encryptFile(filename):       
    plainBlock = getLargeBlock(filename)
    encryptedBlock = []
    lenFill = len(str(len(plainBlock)))

    print("Plain text: ", filename)

    for i in range(len(plainBlock)):
        encryptedBlock.append(encrypt(plainBlock[i], getKey(keyfile)))
        print("Encrypted: " + str(i).zfill(lenFill)+"/" +
              str(len(plainBlock)).zfill(lenFill)+"\r")  # check
    print("Encrypted: "+str(len(plainBlock)))

    finaldata = writeToOutputHex(encryptedBlock)

    print("Encrypted Data: ", finaldata)

    return finaldata


def decryptFile(filename, keyfile1):
    inputBlock = getLargeHexBlock(filename)
    for i in range(len(inputBlock)):
        inputBlock[i] = decrypt(inputBlock[i], getKey(keyfile))
        print("Decrypted: ", str(i).zfill(8)+"/"+str(len(inputBlock)).zfill(8)+"\r")  # check

    finalDecryptdata = writeToOutputPlain(inputBlock)

    print("Decrypted Data: ", finalDecryptdata)

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