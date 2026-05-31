from rest_framework import serializers

from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):

    category = serializers.StringRelatedField()
    account = serializers.StringRelatedField()

    class Meta:

        model = Transaction

        fields = [

            'id',
            'category',
            'account',
            'transaction_type',
            'amount',
            'transaction_date',
            'description',
        ]
