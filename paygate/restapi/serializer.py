from rest_framework import serializers


class TransactSerializer(serializers.Serializer):
    cvv = serializers.IntegerField(min_value=100, max_value=999)
    card_number = serializers.IntegerField(max_length=16)
    exp_date = serializers.DateField()
    amount = serializers.IntegerField(min_value=1)