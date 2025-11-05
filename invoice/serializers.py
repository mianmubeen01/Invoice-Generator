from rest_framework import serializers
from .models import Company, Client, Invoice, InvoiceItems

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"


class InvoiceItemSerializer(serializers.ModelSerializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, default=0.00, read_only=True)
    tax_percentage = serializers.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    total = serializers.DecimalField(max_digits=10, decimal_places=2, default=0.00, read_only=True)

    class Meta:
        model = InvoiceItems
        fields = "__all__"
        read_only_fields = ["subtotal", "total"]
    
    
    def create(self, validated_data):
        item = InvoiceItems.objects.create(**validated_data)
        return item



class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ["invoice_no", "invoice_date", "due_date"]
      


