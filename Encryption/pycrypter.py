from argparse import *
import os.path
from datetime import datetime
from readKeyFile import *
from readBlockFile import *
from AES256 import encrypt, decrypt


def encryptFile(filename, keyfile):
    plainBlock = getLargeBlock(filename)
    encryptedBlock = []
    lenFill = len(str(len(plainBlock)))
    boolWritten = False
    for i in range(len(plainBlock)):
        encryptedBlock.append(encrypt(plainBlock[i], getKey(keyfile)))
        print("Encrypted: " + str(i).zfill(lenFill)+"/" +
              str(len(plainBlock)).zfill(lenFill)+"\r")  # check
    print("Encrypted: "+str(len(plainBlock)))
    # return encryptedBlock

    finaldata = writeToOutputHex(encryptedBlock)
    return finaldata


def decryptFile(filename, keyfile):
    inputBlock = getLargeHexBlock(filename)
    boolWritten = False
    for i in range(len(inputBlock)):
        inputBlock[i] = decrypt(inputBlock[i], getKey(keyfile))
        print(str(i).zfill(8)+"/"+str(len(inputBlock)).zfill(8)+"\r")  # check

    finalDecryptdata = writeToOutputPlain(inputBlock)

    return finalDecryptdata


def writeToOutputPlain(block):
    # outputFile = open(outputFilename, "w")
    outputFile = ""

    lenFill = len(str(len(block)))
    k = 0
    while k < len(block):
        for j in range(0, len(block[k])):
            outputFile += chr(block[k][j])

        k += 1

    return outputFile


def writeToOutputHex(block):
    # outputFile = open(outputFilename, "w")
    outputFile = ""
    k = 0
    lenFill = len(str(len(block)))
    while k < len(block):
        for j in range(0, len(block[k])):
            outputFile += (hex(block[k][j]))[2:].zfill(2)

        k += 1

    return outputFile
    # return True


def Main():

    blockFile = input("Enter text to encrypt: ")

    # This is a 256-bit hexxadecimal key
    keyFile = "576E5A7234753778214125442A472D4B614E645267556B58703273357638792F"

    # operation = str(args.operation).lower()

    enc_text = encryptFile(blockFile, keyFile)
    print("Encrypted data: ", enc_text)

    dec_text = decryptFile(enc_text, keyFile)
    print("Decrypted data: ", dec_text)


Main()
