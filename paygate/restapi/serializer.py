from rest_framework import serializers


class TransactSerializer(serializers.Serializer):
    cvv = serializers.IntegerField(min_value=100, max_value=999)
    sender_accno = serializers.IntegerField()
    exp_date = serializers.CharField()
    amount = serializers.IntegerField(min_value=1)
    rec_accno = serializers.IntegerField()