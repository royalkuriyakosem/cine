from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductionViewSet, SceneViewSet, ShotViewSet, BudgetLineViewSet

router = DefaultRouter()
router.register(r'productions', ProductionViewSet)
router.register(r'scenes', SceneViewSet)
router.register(r'shots', ShotViewSet)
router.register(r'budget-lines', BudgetLineViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
