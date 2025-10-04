from rest_framework import serializers
from .models import Invoice, Contract

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'
        read_only_fields = ('paid',)

class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = '__all__'
        read_only_fields = ('expiry_alert_sent',)