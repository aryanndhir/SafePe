from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse
from paygate.restapi.serializer import TransactSerializer
from paygate.views import sender_bank, receiver_bank
from paygate.Encryption import aes, ecc
import numpy as np


@api_view(['POST'])
def transact(request):

    if request.method == 'POST':
        serializer = TransactSerializer(data = request.data)
        if serializer.is_valid():
            sender_accno = str(serializer.data['sender_accno'])
            cvv = str(serializer.data['cvv'])
            expirydate = serializer.data['exp_date']
            amount = str(serializer.data['amount'])
            receiver_accno = str(serializer.data['rec_accno'])

            data = sender_accno + "," + cvv + "," + amount + "," + expirydate + "," + receiver_accno

            aes_data = aes.encryptFile(data)
            aes_key = aes.keyfile
            aes_ecc_key = ecc.encrypt_data(aes_key, "sender")

            sender_verification = sender_bank(aes_ecc_key, aes_data)

            if type(sender_verification) == np.int64:
                aes_ecc_key = ecc.encrypt_data(aes_key, "receiver")
                receiver_verification = receiver_bank(aes_ecc_key, aes_data)

                if type(receiver_verification) == np.int64:
                    
                    msg = {
                        'sender balance': sender_verification.item(),
                        'receiver balance': receiver_verification.item()
                    }

                    return JsonResponse(msg, status=status.HTTP_201_CREATED, safe=False)
                else:
                    return Response(receiver_verification, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(sender_verification, status=status.HTTP_400_BAD_REQUEST)

        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



