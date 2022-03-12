from sqlalchemy import true
import aes
import ecc


def sender_bank():
    return true

def receiver_bank():
    pass


# data to be encoded {Account number, CVV, Amount, Expiry date} -> Input
# print(keyfile)

def PaymentGateway():

    concatStr = AccNo + CVV + Amount + ExpiryDate
    aes_data = aes.encryptFile(concatStr)
    aes_key = aes.keyfile
    ecc_data = ecc.encrypt_data(aes_key)

    verification = sender_bank(ecc_data, aes_data)

    if(verification):
        receiver_bank(ecc_data, aes_data)
    else:
        print("Payment Failed")
