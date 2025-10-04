from rest_framework import serializers
from .models import CallSheet, DailyProductionReport, CrewCheckIn

class CallSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallSheet
        fields = '__all__'
        read_only_fields = ('published',)

class DailyProductionReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyProductionReport
        fields = '__all__'

class CrewCheckInSerializer(serializers.ModelSerializer):
    crew_member_username = serializers.CharField(source='crew_member.username', read_only=True)

    class Meta:
        model = CrewCheckIn
        fields = ('id', 'call_sheet', 'crew_member', 'check_in_time', 'crew_member_username')
        read_only_fields = ('crew_member', 'check_in_time')