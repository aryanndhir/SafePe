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

    accNo = int(accNo)
    cvv = int(cvv)
    amount = int(amount)

    # print("find: ", df.loc[df['accountno'] == accNo])
    # exx = df.loc[df['accountno'] == accNo]['expirydate'].values[0]
    # print("exx", exx)
    # print("exx type: ", type(exx))

    expiryDate = datetime.strptime(expiryDate, '%d/%m/%y')
    expiryDate = np.datetime64(expiryDate)
    todayDate = np.datetime64(date.today())

    # print("expiryDate", expiryDate)
    # print("expiry type", type(expiryDate))
    # print(expiryDate > exx)

    bank_record = df.loc[df['accountno'] == accNo]
    bank_record_cvv = bank_record['cvv'].values[0]
    bank_record_amount = bank_record['amount'].values[0]
    bank_record_expiryDate = bank_record['expirydate'].values[0]

    if(bank_record.empty):
        return false
    else:
        if bank_record_cvv == cvv:
        # if bank_record['cvv'].values[0] == cvv:
            
            if bank_record_amount >= amount:
            # if df.loc[df['accountno'] == accNo]['amount'].values[0] >= int(amount):

                if bank_record_expiryDate == expiryDate and expiryDate >= todayDate:
                # if df.loc[df['accountno'] == accNo]['expirydate'].values[0] == expiryDate:
                    
                    df.loc[df['accountno'] == accNo, 'amount'] = bank_record_amount - int(amount)                    
                    # df.loc[df['accountno'] == accNo, 'amount'] = df.loc[df['accountno'] == accNo]['amount'].values[0] - int(amount)
                    
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