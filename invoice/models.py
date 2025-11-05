from django.db import models
from decimal import Decimal
from datetime import timedelta
from django.utils import timezone
# Create your models here.

def Default_due_date():
    return timezone.now().date() + timedelta(days=10)


class Company(models.Model):
    country_choices = [
        ('USA', 'United States of America'),
        ('CAN', 'Canada'),
        ('MEX', 'Mexico'),
        ('GBR', 'United Kingdom'),
        ('FRA', 'France'),
    ]


    company_name = models.CharField(max_length=30)
    name = models.CharField(max_length=20)
    address = models.CharField(max_length=50, null=True, blank=True)
    city_zipcode = models.CharField(max_length=20)
    country = models.CharField(max_length=5, choices=country_choices)

    def __str__(self):
        return f"{self.name} - {self.company_name}"

class Client(models.Model):
    country_choices = [
        ('USA', 'United States of America'),
        ('CAN', 'Canada'),
        ('MEX', 'Mexico'),
        ('GBR', 'United Kingdom'),
        ('FRA', 'France'),
    ]

    company_name = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    address = models.CharField(max_length=50, null=True, blank=True)
    city_zipcode = models.CharField(max_length=20)
    country = models.CharField(max_length=5, choices=country_choices)

    def __str__(self):
        return f"{self.name} - {self.company_name}"


class Invoice(models.Model):
    invoice_no = models.CharField(max_length=50)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
    invoice_date = models.DateField()
    due_date = models.DateField(default=Default_due_date)

    def __str__(self):
        return f"{self.invoice_no} - {self.invoice_date} - {self.due_date}"

class InvoiceItems(models.Model):
    description = models.TextField()
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="items")
    quantity = models.IntegerField()
    rate = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    
    def amount(self):
        return self.quantity * self.rate
    
    def calculate_subtotal(self):
        return sum(item.amount() for item in InvoiceItems.objects.filter(invoice=self.invoice))

    def calculate_tax(self):
        subtotal = self.calculate_subtotal()
        return (subtotal * self.tax_percentage) / 100

    def calculate_total(self):
        return self.calculate_subtotal() + self.calculate_tax()
    
    def save(self, *args, **kwargs):
        self.subtotal = self.calculate_subtotal()
        self.total = self.calculate_total()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.description} - {self.invoice}"
