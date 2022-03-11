from pycrypter import encryptFile, decryptFile
import ecc_eceispy


# data to be encoded {Account number, CVV, Amount, Expiry date} -> Input

def PaymetGateway():
    concatStr = AccNo + CVV + Amount + ExpiryDate
    encData = encryptFile(concaStr)
