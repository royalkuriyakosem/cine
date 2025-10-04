from django.contrib import admin
from .models import VFXShot, Asset, ShotVersion

@admin.register(VFXShot)
class VFXShotAdmin(admin.ModelAdmin):
    list_display = ('shot', 'production', 'status', 'assigned_team', 'due_date')
    list_filter = ('status', 'production')
    search_fields = ('assigned_team',)

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('name', 'uploaded_by', 'uploaded_at')
    list_filter = ('uploaded_at',)
    search_fields = ('name',)

@admin.register(ShotVersion)
class ShotVersionAdmin(admin.ModelAdmin):
    list_display = ('vfx_shot', 'version_number', 'uploaded_at', 'approved')
    list_filter = ('approved', 'uploaded_at')
    search_fields = ('notes',)
