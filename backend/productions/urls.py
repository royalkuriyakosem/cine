from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ExampleProductionView, ProductionViewSet, SceneViewSet, ShotViewSet, BudgetLineViewSet

router = DefaultRouter()
router.register(r'productions', ProductionViewSet)
router.register(r'scenes', SceneViewSet)
router.register(r'shots', ShotViewSet)
router.register(r'budget-lines', BudgetLineViewSet)

urlpatterns = [
    path('', ExampleProductionView.as_view()),
] + router.urls
