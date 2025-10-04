from celery import shared_task
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.contrib.auth import get_user_model
import os
import shutil
from .models import Asset

User = get_user_model()
TEMP_UPLOAD_DIR = os.path.join(settings.MEDIA_ROOT, 'tmp_uploads')

@shared_task
def assemble_file_chunks(upload_id, total_chunks, final_path):
    upload_dir = os.path.join(TEMP_UPLOAD_DIR, upload_id)
    content_file = ContentFile(b"")
    
    for i in range(total_chunks):
        chunk_path = os.path.join(upload_dir, f"{i}.part")
        with open(chunk_path, 'rb') as chunk_file:
            content_file.write(chunk_file.read())
    
    saved_path = default_storage.save(final_path, content_file)
    shutil.rmtree(upload_dir)
    return saved_path

@shared_task
def create_asset_from_file(saved_path, file_name, user_id):
    user = User.objects.get(id=user_id)
    asset = Asset.objects.create(
        name=file_name,
        file=saved_path,
        uploaded_by=user
    )
    return f"Asset {asset.id} created for file {saved_path}"

@shared_task
def process_chunked_upload(file_id, original_filename, total_chunks, user_id):
    """Process uploaded chunks and create an Asset"""
    chunks_dir = os.path.join(settings.MEDIA_ROOT, 'chunks', file_id)
    final_path = os.path.join(settings.MEDIA_ROOT, 'vfx/assets', original_filename)
    
    # Combine chunks
    with open(final_path, 'wb') as outfile:
        for i in range(total_chunks):
            chunk_path = os.path.join(chunks_dir, f'chunk_{i}')
            with open(chunk_path, 'rb') as infile:
                outfile.write(infile.read())
    
    # Create asset
    user = get_user_model().objects.get(id=user_id)
    asset = Asset.objects.create(
        name=original_filename,
        file=f'vfx/assets/{original_filename}',
        uploaded_by=user
    )
    
    # Cleanup chunks
    shutil.rmtree(chunks_dir)
    
    return f"Asset {asset.id} created from chunks"