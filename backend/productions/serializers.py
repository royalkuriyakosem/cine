from rest_framework import serializers
from .models import Production, Scene, Shot, BudgetLine, ScriptBreakdown, BudgetPrediction

class ProductionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Production
        fields = '__all__'
        read_only_fields = ('owner',)

class SceneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scene
        fields = '__all__'

class ShotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shot
        fields = '__all__'

class BudgetLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetLine
        fields = '__all__'

class BudgetPredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetPrediction
        fields = '__all__'
