from django.db import models
from decimal import Decimal
from datetime import timedelta
from django.utils import timezone

def default_due_date():
    return timezone.now().date() + timedelta(days=10)


class Company(models.Model):
    country_choices = [
        ('USA', 'United States of America'),
        ('CAN', 'Canada'),
        ('MEX', 'Mexico'),
        ('GBR', 'United Kingdom'),
        ('FRA', 'France'),
    ]
    logo = models.ImageField(upload_to="uploads", default=None)
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
    address = models.CharField(max_length=50, null=True, blank=True)
    city_zipcode = models.CharField(max_length=20)
    country = models.CharField(max_length=5, choices=country_choices)

    def __str__(self):
        return self.company_name


class Invoice(models.Model):
    invoice_no = models.CharField(max_length=50)
    invoice_title = models.CharField(max_length=30, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
    invoice_date = models.DateField()
    due_date = models.DateField(default=default_due_date)

    def subtotal(self):
        return sum(item.amount() for item in self.items.all())

    def tax_total(self):
        return sum(item.tax_amount() for item in self.items.all())

    def grand_total(self):
        return self.subtotal() + self.tax_total()

    def __str__(self):
        return f"{self.invoice_no} - {self.invoice_date}"


class InvoiceItem(models.Model):
    description = models.TextField()
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="items")
    quantity = models.IntegerField()
    rate = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    def amount(self):
        return self.quantity * self.rate

    def tax_amount(self):
        return (self.amount() * self.tax_percentage) / 100

    def __str__(self):
        return f"{self.description} - {self.invoice}"
