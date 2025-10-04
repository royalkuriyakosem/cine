from rest_framework import serializers
from .models import VFXShot, Asset, ShotVersion

class VFXShotSerializer(serializers.ModelSerializer):
    class Meta:
        model = VFXShot
        fields = '__all__'

class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = '__all__'
        read_only_fields = ('uploaded_by',)

class ShotVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShotVersion
        fields = '__all__'
        read_only_fields = ('approved', 'approved_by')