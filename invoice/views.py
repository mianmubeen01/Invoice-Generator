from .models import Invoice
from .serializers import  InvoiceSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
# Create your views here.
class InvoiceView(viewsets.ModelViewSet):
    serializer_class = InvoiceSerializer
    queryset = Invoice.objects.all()
    
    def create(self, request, *args, **Kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception =True)
        serializer.save()
        return Response(
            {"message": "Invoice Created Succesfully", 
            "data": serializer.data}, status=status.HTTP_201_CREATED
        )
