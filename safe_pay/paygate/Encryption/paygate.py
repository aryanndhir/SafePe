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

    expiryDate = datetime.strptime(expiryDate, '%d/%m/%y')
    expiryDate = np.datetime64(expiryDate)
    todayDate = np.datetime64(date.today())

    bank_record = df.loc[df['accountno'] == accNo]
    bank_record_cvv = bank_record['cvv'].values[0]
    bank_record_amount = bank_record['amount'].values[0]
    bank_record_expiryDate = bank_record['expirydate'].values[0]

    if(bank_record.empty):
        return false
    else:
        if bank_record_cvv == cvv:
            
            if bank_record_amount >= amount and amount > 0:

                if bank_record_expiryDate == expiryDate and expiryDate >= todayDate:
                    
                    df.loc[df['accountno'] == accNo, 'amount'] = bank_record_amount - int(amount)                    
                    # df.to_excel("bank_records.xlsx", index=False)
                    return true

    return false


def receiver_bank(aes_ecc_key, aes_data):
    
    aes_key = ecc.decrypt_data(aes_ecc_key, "receiver")
    data = aes.decryptFile(aes_data, aes_key)

    accNo, cvv, amount, expiryDate, recAccNo  =  data.split(",")
    # recAccNo = int(recAccNo)

    # df = pd.read_excel("bank_records.xlsx")

    # bank_record = df.loc[df['accountno'] == recAccNo]

    # if(bank_record.empty):
    #     return false
    # else:

    #     if amount > 0:
    #         bank_record_amount = bank_record['amount'].values[0]
    #         df.loc[df['accountno'] == recAccNo, 'amount'] = bank_record_amount + amount
    #         # df.to_excel("bank_records.xlsx", index=False)
    #         return true

    return false


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
data = "7731760391,112,50,18/12/25,2908566021"
PaymentGateway(data)