from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Production, Scene, Shot, BudgetLine
from .serializers import ProductionSerializer, SceneSerializer, ShotSerializer, BudgetLineSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

class ProductionViewSet(viewsets.ModelViewSet):
    queryset = Production.objects.all()
    serializer_class = ProductionSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['title', 'description']
    filterset_fields = ['status', 'owner']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class SceneViewSet(viewsets.ModelViewSet):
    queryset = Scene.objects.all()
    serializer_class = SceneSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['production']

class ShotViewSet(viewsets.ModelViewSet):
    queryset = Shot.objects.all()
    serializer_class = ShotSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['scene', 'status', 'assigned_to']

class BudgetLineViewSet(viewsets.ModelViewSet):
    queryset = BudgetLine.objects.all()
    serializer_class = BudgetLineSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['production', 'approved']

class ExampleProductionView(APIView):
    def get(self, request):
        return Response({"message": "Productions endpoint"})
