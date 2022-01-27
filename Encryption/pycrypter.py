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

    # boolWritten = writeToOutputHex(encryptedBlock, outputFile)
    # if boolWritten == True:
    #     return "Successfully encrypted: " + filename + " with key: " + keyfile + " into: " + outputFile
    # else:
    #     return "Something went wrong, please check settings"


def decryptFile(filename, keyfile):
    inputBlock = getLargeHexBlock(filename)
    boolWritten = False
    for i in range(len(inputBlock)):
        inputBlock[i] = decrypt(inputBlock[i], getKey(keyfile))
        print(str(i).zfill(8)+"/"+str(len(inputBlock)).zfill(8)+"\r")  # check

    finalDecryptdata = writeToOutputPlain(inputBlock)

    return finalDecryptdata

    # boolWritten = writeToOutputPlain(inputBlock, outputFile)
    # if boolWritten == True:
    #     return "Successfully decrypted: " + filename + " with: " + keyfile + " into: " + outputFile
    # else:
    #     return "Something went wrong, please check settings"
    
    # return inputBlock


def writeToOutputPlain(block):
    # outputFile = open(outputFilename, "w")
    outputFile = ""

    lenFill = len(str(len(block)))
    k = 0
    while k < len(block):
        for j in range(0, len(block[k])):
            outputFile += chr(block[k][j])
            # outputFile.write(chr(block[k][j]))
        # print("Written: "+str(k).zfill(lenFill)+"/"+str(len(block)) +
            #   " to file "+outputFilename+" \r")  # check
        k += 1
    # outputFile.close()
    # return True
    return outputFile


def writeToOutputHex(block):
    # outputFile = open(outputFilename, "w")
    outputFile = ""
    k = 0
    lenFill = len(str(len(block)))
    while k < len(block):
        for j in range(0, len(block[k])):
            outputFile += (hex(block[k][j]))[2:].zfill(2)
            # outputFile.write(hex(block[k][j])[2:].zfill(2))
        
        # print("Written: "+str(k).zfill(lenFill)+"/"+str(len(block)) +
            #   " to file "+outputFilename+" \r")  # check
        k += 1
    # print("Written: "+str(len(block)).zfill(lenFill) +
        #   " to file "+outputFilename)  # check
    # outputFile.close()
    return outputFile
    # return True


# def is_valid_file(parser, arg):
#     if not os.path.exists(arg):
#         parser.error("The file %s does not exist!" % arg)
#     else:
#         return arg


def Main():
    # parser = ArgumentParser(description='''
    # Parser''', formatter_class=RawDescriptionHelpFormatter)
    # parser.add_argument('operation', metavar="operation",
    #                     type=str, help="Either input (Encrypt/Decrypt) or (E/D)")
    # parser.add_argument('filename', metavar="filename", type=lambda x: is_valid_file(
    #     parser, x), help="Filename for file to be encrypted ex: blockfile.txt")
    # parser.add_argument('keyfile', metavar="keyfile", type=lambda x: is_valid_file(
    #     parser, x), help="Keyfile with 32 byte key ex: keyfile.txt")
    # parser.add_argument('-o', '--output', metavar="filename", type=str,
    #                     help="Output filename for encrypted or decrypted file default: output.txt")
    # args = parser.parse_args()

    blockFile = input("Enter text to encrypt: ")

    # This is a 256-bit hexxadecimal key
    keyFile = "576E5A7234753778214125442A472D4B614E645267556B58703273357638792F"
    
    # operation = str(args.operation).lower()

    enc_text = encryptFile(blockFile, keyFile)
    print("Encrypted data: ", enc_text)

    dec_text = decryptFile(enc_text, keyFile)
    print("Decrypted data: ", dec_text)


    # if not args.output:
    #     output = "output.txt"
    # else:
    #     output = args.output
    # startTime = datetime.now()
    # if operation == "encrypt" or operation == "e":
    #     status = encryptFile(blockFile, keyFile, output)
    # elif operation == "decrypt" or operation == "d":
    #     status = decryptFile(blockFile, keyFile, output)
    # executionTime = datetime.now() - startTime

    # print(status + "\nExecution time: " + str(executionTime))  # check


Main()
