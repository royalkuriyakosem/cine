from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VFXShotViewSet, AssetViewSet, ShotVersionViewSet, AssetUploadView, VersionUploadView

router = DefaultRouter()
router.register(r'shots', VFXShotViewSet)
router.register(r'assets', AssetViewSet)
router.register(r'versions', ShotVersionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('assets/initiate-upload/', AssetUploadView.as_view(), name='initiate-asset-upload'),
    path('versions/initiate-upload/', VersionUploadView.as_view(), name='initiate-version-upload'),
]
