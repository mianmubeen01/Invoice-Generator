from django.shortcuts import render
from .models import Company, Client, Invoice, InvoiceItems
from .serializers import CompanySerializer, ClientSerializer, InvoiceSerializer, InvoiceItemSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# Create your views here.
class InvoiceView(APIView):
    def post(self, request):
        data = request.data
        
        company_data = data.get("company")
        company_serializer = CompanySerializer(data=company_data)
        company_serializer.is_valid(raise_exception=True)
        company = company_serializer.save()

        client_data = data.get("client")
        client_serializer = ClientSerializer(data=client_data)
        client_serializer.is_valid(raise_exception=True)
        client = client_serializer.save()

        invoice_data = data.get("invoice")
        invoice_data["company"] = company.id
        invoice_data["client"] = client.id
        invoice_serializer = InvoiceSerializer(data=invoice_data)
        invoice_serializer.is_valid(raise_exception=True)
        invoice = invoice_serializer.save()

        items_data = data.get("items")
        created_items = []
        for item in items_data:
            item["invoice"] = invoice.id
            item_serializer = InvoiceItemSerializer(data=item)
            item_serializer.is_valid(raise_exception=True)
            item_serializer.save()
            created_items.append(item_serializer.data)

        return Response(
            {
                "message": "Invoice created successfully",
                "company": company_serializer.data,
                "client": client_serializer.data,
                "invoice": invoice_serializer.data,
                "items": created_items,
            },
            status=status.HTTP_201_CREATED,
        )
