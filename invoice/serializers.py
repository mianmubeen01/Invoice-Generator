from rest_framework import serializers
from .models import Company, Client, Invoice, InvoiceItem

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['company_name', 'name', 'address', 'city_zipcode', 'country', 'logo']

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['company_name', 'address', 'city_zipcode', 'country']

class InvoiceItemSerializer(serializers.ModelSerializer):
    amount = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = InvoiceItem
        fields = ['description', 'quantity', 'rate', 'tax_percentage', 'amount']

    def get_amount(self, obj):
        return obj.amount()

class InvoiceSerializer(serializers.ModelSerializer):
    company = CompanySerializer()
    client = ClientSerializer()
    items = InvoiceItemSerializer(many=True)

    class Meta:
        model = Invoice
        fields = ['id', 'invoice_no', 'invoice_title', 'invoice_date', 'due_date',
                  'company', 'client', 'items']

    def create(self, validated_data):
        
        company_data = validated_data.pop('company')
        client_data = validated_data.pop('client')
        items_data = validated_data.pop('items')

        request = self.context.get('request')
        if request and request.FILES.get('company.logo'):
            company_data['logo'] = request.FILES['company.logo']

        company = Company.objects.create(**company_data)
        client = Client.objects.create(**client_data)
        invoice = Invoice.objects.create(company=company, client=client, **validated_data)

        for item_data in items_data:
            InvoiceItem.objects.create(invoice=invoice, **item_data)

        return invoice

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['subtotal'] = instance.subtotal()
        data['tax'] = instance.tax_total()
        data['total'] = instance.grand_total()
        return data
