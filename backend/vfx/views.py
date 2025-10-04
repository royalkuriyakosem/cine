from rest_framework import viewsets, status, views
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from .models import VFXShot, Asset, ShotVersion
from .serializers import VFXShotSerializer, AssetSerializer, ShotVersionSerializer
from .permissions import IsPostProdOrAssigned

class VFXShotViewSet(viewsets.ModelViewSet):
    queryset = VFXShot.objects.all()
    serializer_class = VFXShotSerializer
    permission_classes = [IsAuthenticated]

class AssetViewSet(viewsets.ModelViewSet):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)

class ShotVersionViewSet(viewsets.ModelViewSet):
    queryset = ShotVersion.objects.all()
    serializer_class = ShotVersionSerializer
    permission_classes = [IsAuthenticated, IsPostProdOrAssigned]

    def perform_create(self, serializer):
        instance = serializer.save()
        # Webhook-style notification stub
        print(f"NOTIFICATION: New version {instance.version_number} uploaded for {instance.vfx_shot}.")
        # In a real app, you would trigger a Celery task here to send an email or a webhook.

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        version = self.get_object()
        version.approved = True
        version.approved_by = request.user
        version.save()
        return Response({'status': 'Version approved'})

class AssetUploadView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        This endpoint provides a hint for resumable uploads.
        It doesn't implement the full upload logic but shows how you might start the process.
        """
        file_name = request.data.get('file_name')
        file_size = request.data.get('file_size')

        if not file_name or not file_size:
            return Response(
                {"error": "file_name and file_size are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # In a real implementation, you would:
        # 1. Generate a unique upload ID.
        # 2. Store initial metadata in Redis or a temporary model.
        # 3. Return a signed URL (e.g., for S3) or the upload ID for chunked uploads.
        
        upload_id = "mock-upload-id-12345"
        upload_url = f"/api/vfx/assets/upload/chunk/{upload_id}/"

        return Response({
            "message": "Upload session initiated. Send file chunks to the provided URL.",
            "upload_id": upload_id,
            "chunk_upload_url": upload_url,
        }, status=status.HTTP_201_CREATED)
