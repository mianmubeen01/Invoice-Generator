from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("api", views.InvoiceView, basename="invoice")


urlpatterns = [
    # path('invoice/', views.InvoiceView.as_view(), name='invoice')
    path('', include(router.urls))
]