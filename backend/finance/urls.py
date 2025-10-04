from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InvoiceViewSet, ContractViewSet

router = DefaultRouter()
router.register(r'invoices', InvoiceViewSet, basename='invoice')
router.register(r'contracts', ContractViewSet, basename='contract')

urlpatterns = [
    path('', include(router.urls)),
]
