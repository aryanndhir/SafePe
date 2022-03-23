from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse
from paygate.restapi.serializer import TransactSerializer
from paygate.views import sender_bank, receiver_bank
from paygate.Encryption import aes, ecc
import numpy as np
import time
import tracemalloc
import logging

logger = logging.getLogger(__name__)


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

            start_enc_timer = time.time()
            tracemalloc.start()

            aes_data = aes.encryptFile(data)
            aes_key = aes.keyfile
            aes_ecc_key = ecc.encrypt_data(aes_key, "sender")

            end_enc_timer = time.time()
            encryption_time = end_enc_timer - start_enc_timer
            logger.warning("Encryption time: %s seconds", encryption_time)

            snapshot = tracemalloc.take_snapshot()
            top_stats = snapshot.statistics('lineno')
            total = sum(stat.size for stat in top_stats)
            logger.warning("Memory consumed in Encryption: %.1f KB" % (total / 1024))
            tracemalloc.stop()

            sender_verification = sender_bank(aes_ecc_key, aes_data, start_enc_timer)

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



