from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
import boto3
from botocore.exceptions import ClientError
import uuid
from .models import Asset
from .tasks import process_chunked_upload

class S3MultipartUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def get_s3_client(self):
        return boto3.client('s3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME,
            endpoint_url=settings.AWS_S3_ENDPOINT_URL
        )

    def post(self, request):
        if not settings.USE_S3:
            return Response(
                {"error": "S3 storage is not configured"},
                status=status.HTTP_501_NOT_IMPLEMENTED
            )

        file_name = request.data.get('fileName')
        file_type = request.data.get('fileType')
        if not file_name or not file_type:
            return Response(
                {"error": "fileName and fileType are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Generate a unique key for the file
        key = f"media/vfx/uploads/{uuid.uuid4()}/{file_name}"
        
        try:
            s3_client = self.get_s3_client()
            mpu = s3_client.create_multipart_upload(
                Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                Key=key,
                ContentType=file_type
            )

            return Response({
                "uploadId": mpu["UploadId"],
                "key": key,
                "partSize": 5 * 1024 * 1024  # 5MB chunks
            })
        except ClientError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class S3UploadPartView(APIView):
    permission_classes = [IsAuthenticated]

    def get_presigned_url(self, key, upload_id, part_number):
        s3_client = boto3.client('s3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME,
            endpoint_url=settings.AWS_S3_ENDPOINT_URL
        )
        
        return s3_client.generate_presigned_url(
            'upload_part',
            Params={
                'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                'Key': key,
                'UploadId': upload_id,
                'PartNumber': part_number
            },
            ExpiresIn=3600
        )

    def post(self, request):
        key = request.data.get('key')
        upload_id = request.data.get('uploadId')
        part_number = request.data.get('partNumber')

        if not all([key, upload_id, part_number]):
            return Response(
                {"error": "key, uploadId, and partNumber are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            presigned_url = self.get_presigned_url(key, upload_id, part_number)
            return Response({"presignedUrl": presigned_url})
        except ClientError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ChunkedUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        chunk = request.FILES.get('chunk')
        chunk_number = int(request.POST.get('chunkNumber'))
        total_chunks = int(request.POST.get('totalChunks'))
        file_id = request.POST.get('fileId')
        original_filename = request.POST.get('originalFilename')

        if not all([chunk, chunk_number, total_chunks, file_id, original_filename]):
            return Response(
                {"error": "Missing required fields"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Start processing task for last chunk
        if chunk_number == total_chunks - 1:
            process_chunked_upload.delay(
                file_id,
                original_filename,
                total_chunks,
                request.user.id
            )
            return Response({"status": "Processing started"})
        
        return Response({"status": "Chunk received"})