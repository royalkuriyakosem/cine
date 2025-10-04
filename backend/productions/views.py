from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Production, Scene, Shot, BudgetLine, ScriptBreakdown
from .serializers import ProductionSerializer, SceneSerializer, ShotSerializer, BudgetLineSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from .services import analyze_script

class ProductionViewSet(viewsets.ModelViewSet):
    queryset = Production.objects.all()
    serializer_class = ProductionSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['title', 'description']
    filterset_fields = ['status', 'owner']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'])
    def breakdown(self, request, pk=None):
        """
        Accept script text and return/save breakdown analysis.
        """
        production = self.get_object()
        script_text = request.data.get('script_text')
        
        if not script_text:
            return Response(
                {"error": "script_text is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Analyze the script
        analysis = analyze_script(script_text)

        # Save the breakdown
        breakdown = ScriptBreakdown.objects.create(
            production=production,
            raw_text=script_text,
            **analysis
        )

        return Response({
            "id": breakdown.id,
            "created_at": breakdown.created_at,
            **analysis
        })

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
