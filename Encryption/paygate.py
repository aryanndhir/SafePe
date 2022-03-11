from pycrypter import encryptFile, decryptFile, keyfile
import ecc_eceispy


# data to be encoded {Account number, CVV, Amount, Expiry date} -> Input
# print(keyfile)

def PaymetGateway():
    concatStr = AccNo + CVV + Amount + ExpiryDate
    encData = encryptFile(concaStr)
    aes_key = keyfile
