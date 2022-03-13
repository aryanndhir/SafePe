from datetime import date
from sqlalchemy import true, false
import aes
import ecc
import pandas as pd
import numpy as np
from datetime import datetime


def sender_bank(aes_ecc_key, aes_data):
    
    aes_key = ecc.decrypt_data(aes_ecc_key, "sender")
    data = aes.decryptFile(aes_data, aes_key)

    accNo, cvv, amount, expiryDate, rec_accNo  =  data.split(",")

    df = pd.read_excel("bank_records.xlsx")

    # print(df['expirydate'])
    accNo = int(accNo)
    cvv = int(cvv)
    amount = int(amount)

    # print("find: ", df.loc[df['accountno'] == accNo])
    # exx = df.loc[df['accountno'] == accNo]['expirydate'].values[0]
    # print("exx", exx)
    # print("exx type: ", type(exx))

    expiryDate = datetime.strptime(expiryDate, '%d/%m/%y')
    expiryDate = np.datetime64(expiryDate)
    # print("expiryDate", expiryDate)
    # print("expiry type", type(expiryDate))
    # print(expiryDate > exx)

    if(df.loc[df['accountno'] == accNo].empty):
        return false
    else:
        # print("hello1")
        if df.loc[df['accountno'] == accNo]['cvv'].values[0] == cvv:
            # print("hello2")
            if df.loc[df['accountno'] == accNo]['amount'].values[0] >= int(amount):
                # print("hello3")
                if df.loc[df['accountno'] == accNo]['expirydate'].values[0] == expiryDate:
                    # print("hello4")
                    df.loc[df['accountno'] == accNo, 'amount'] = df.loc[df['accountno'] == accNo]['amount'].values[0] - int(amount)
                    # df.to_excel("bank_records.xlsx", index=False)
                    return true

    # check if the account number is valid
    # check if the amount is valid
    # check if the cvv is valid
    # check if the expiry date is valid
    # check if the account has sufficient balance

    return false


def receiver_bank(aes_ecc_key, aes_data):
    
    aes_key = ecc.decrypt_data(aes_ecc_key, "receiver")
    data = aes.decryptFile(aes_data, aes_key)

    recAccNo =  data.split(",")[-1]

    # check if the account number is valid

    return true


def PaymentGateway(data):

    # accNo, cvv, amount, expiryDate =  data.split(",")
    # concatStr = accNo + cvv + amount + expiryDate
    concatStr = data

    aes_data = aes.encryptFile(concatStr)
    aes_key = aes.keyfile
    aes_ecc_key = ecc.encrypt_data(aes_key, "sender")

    verification = sender_bank(aes_ecc_key, aes_data)

    if verification == true:
        aes_ecc_key = ecc.encrypt_data(aes_key, "receiver")
        receiver_bank(aes_ecc_key, aes_data)
        print("Success")
    else:
        print("Payment Failed")


# data = "123456789,123,100,12/12/12,98765432"
data = "7731760391,112,50,18/12/25,98765432"
PaymentGateway(data)