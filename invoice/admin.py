from django.contrib import admin
from .models import Client, Company, Invoice, InvoiceItem
# Register your models here.
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['id', 'name','company_name', 'logo']

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = [ 'id', 'company_name']

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'invoice_no', 'invoice_date', 'due_date']

@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'description', 'quantity', 'rate', 'tax_percentage']