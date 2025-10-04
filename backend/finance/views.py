from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Invoice, Contract
from .serializers import InvoiceSerializer, ContractSerializer
from accounts.permissions import RolePermission

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [RolePermission]
    required_roles = ['PRODUCER', 'FINANCE_LEGAL', 'LINE_PRODUCER']

class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    permission_classes = [RolePermission]
    required_roles = ['PRODUCER', 'FINANCE_LEGAL']

class ExampleFinanceView(APIView):
    def get(self, request):
        return Response({"message": "Finance endpoint"})
