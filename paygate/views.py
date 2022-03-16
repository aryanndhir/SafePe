from django.shortcuts import render
from sqlalchemy import true, false
import pandas as pd
import numpy as np
from datetime import datetime
from datetime import date
from django.contrib import messages
from paygate.Encryption import aes, ecc


def home(request):
    return render(request, 'home.html')


def features(request):
    return render(request, 'features.html')


def doc(request):
    return render(request, 'documentation.html')


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

    if(bank_record.empty):
        return "Sender's account number does not exist"
    else:
        bank_record_cvv = bank_record['cvv'].values[0]
        if bank_record_cvv == cvv:
            
            bank_record_amount = bank_record['amount'].values[0]
            if bank_record_amount >= amount and amount > 0:

                bank_record_expiryDate = bank_record['expirydate'].values[0]
                if bank_record_expiryDate == expiryDate and expiryDate >= todayDate:
                    
                    df.loc[df['accountno'] == accNo, 'amount'] = bank_record_amount - int(amount)                    
                    # df.to_excel("bank_records.xlsx", index=False)
                else:
                    return "Expiry date is incorrect or has passed"
            else:
                return "Insufficient funds"
        else:
            return "Invalid CVV"

    return "success"


def receiver_bank(aes_ecc_key, aes_data):
    
    aes_key = ecc.decrypt_data(aes_ecc_key, "receiver")
    data = aes.decryptFile(aes_data, aes_key)

    accNo, cvv, amount, expiryDate, recAccNo  =  data.split(",")
    
    recAccNo = recAccNo.strip().strip('*\x00') 
    recAccNo = int(recAccNo)
    amount = int(amount)

    df = pd.read_excel("bank_records.xlsx")

    bank_record = df.loc[df['accountno'] == recAccNo]

    if(bank_record.empty):
        return "Receiver's account number does not exist"
    else:
        bank_record_amount = bank_record['amount'].values[0]
        df.loc[df['accountno'] == recAccNo, 'amount'] = bank_record_amount + amount
        # df.to_excel("bank_records.xlsx", index=False)

    return "success"


def pay(request):

    if request.method == "POST":

        form = request.POST

        sender_accno = form['sender_accno']
        cvv = form['sender_cvv']
        amount = form['sender_amount']
        expiryDate = form['sender_expirydate']
        expiryMonth = form['sender_expirymonth']
        expiryYear = form['sender_expiryyear']
        receiver_accno = form['receiver_accno']
        expirydate = expiryDate + "/" + expiryMonth + "/" + expiryYear

        data = sender_accno + "," + cvv + "," + amount + "," + expirydate + "," + receiver_accno
        
        aes_data = aes.encryptFile(data)
        aes_key = aes.keyfile
        aes_ecc_key = ecc.encrypt_data(aes_key, "sender")

        sender_verification = sender_bank(aes_ecc_key, aes_data)

        if sender_verification == "success":
            aes_ecc_key = ecc.encrypt_data(aes_key, "receiver")
            receiver_verification = receiver_bank(aes_ecc_key, aes_data)

            if receiver_verification == "success":
                messages.success(request, 'Payment successful!')
            else:
                messages.error(request, receiver_verification)
        else:
            messages.error(request, sender_verification)

    return render(request, 'payment-page.html')
