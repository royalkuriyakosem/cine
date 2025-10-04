from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VFXShotViewSet, AssetViewSet, ShotVersionViewSet
from .upload import S3MultipartUploadView, S3UploadPartView, ChunkedUploadView

router = DefaultRouter()
router.register(r'shots', VFXShotViewSet)
router.register(r'assets', AssetViewSet)
router.register(r'versions', ShotVersionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('upload/s3/initiate/', S3MultipartUploadView.as_view(), name='s3-upload-initiate'),
    path('upload/s3/part/', S3UploadPartView.as_view(), name='s3-upload-part'),
    path('upload/chunked/', ChunkedUploadView.as_view(), name='chunked-upload'),
]
