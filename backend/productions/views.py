from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Production, Scene, Shot, BudgetLine, ScriptBreakdown
from .serializers import ProductionSerializer, SceneSerializer, ShotSerializer, BudgetLineSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from .services import analyze_script
from .budget import predict_budget_for_production
from .serializers import BudgetPredictionSerializer
from .ai_service import generate_schedule_from_script # Import the new service

class ProductionViewSet(viewsets.ModelViewSet):
    queryset = Production.objects.all()
    serializer_class = ProductionSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['title', 'description']
    filterset_fields = ['status', 'owner']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'], url_path='predict-budget')
    def predict_budget(self, request, pk=None):
        """
        Generates a budget prediction for the production based on a simple heuristic.
        """
        production = self.get_object()
        prediction = predict_budget_for_production(production)
        serializer = BudgetPredictionSerializer(prediction)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def breakdown(self, request, pk=None):
        """
        Accepts script text, generates a production schedule using AI,
        and returns the schedule as JSON.
        """
        script_text = request.data.get('script_text')
        
        if not script_text:
            return Response(
                {"error": "script_text is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Generate the schedule using the AI service
            schedule_data = generate_schedule_from_script(script_text)
            return Response(schedule_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": f"Failed to generate schedule: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_SERVICE_UNAVAILABLE
            )

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
