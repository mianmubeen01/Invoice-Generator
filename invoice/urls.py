from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path('invoice/', views.InvoiceView.as_view(), name='invoice')
]