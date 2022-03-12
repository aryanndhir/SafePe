from sqlalchemy import true
import aes
import ecc


def sender_bank(aes_ecc_key, aes_data):
    
    aes_key = ecc.decrypt_data(aes_ecc_key, "sender")
    data = aes.decryptFile(aes_data, aes_key)

    print("Data: ", data)

    accNo, cvv, amount, expiryDate =  data.split(",")

    # check if the account number is valid
    # check if the amount is valid
    # check if the CVV is valid
    # check if the expiry date is valid
    # check if the account is active
    # check if the account has sufficient balance

    return true


def receiver_bank(aes_ecc_key, aes_data):
    
    aes_key = ecc.decrypt_data(aes_ecc_key, "receiver")
    data = aes.decryptFile(aes_data, aes_key)

    accNo, cvv, amount, expiryDate =  data.split(",")


# data to be encoded {Account number, CVV, Amount, Expiry date} -> Input
# print(keyfile)


def PaymentGateway(data):

    # accNo, cvv, amount, expiryDate =  data.split(",")
    # concatStr = accNo + cvv + amount + expiryDate
    concatStr = data

    aes_data = aes.encryptFile(concatStr)
    aes_key = aes.keyfile
    aes_ecc_key = ecc.encrypt_data(aes_key, "sender")

    verification = sender_bank(aes_ecc_key, aes_data)

    if(verification):
        aes_ecc_key = ecc.encrypt_data(aes_key, "receiver")
        receiver_bank(aes_ecc_key, aes_data)
        print("Success")
    else:
        print("Payment Failed")


data = "123456789,123,100,12/12"
PaymentGateway(data)

