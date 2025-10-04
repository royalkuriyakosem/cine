from django.contrib import admin
from .models import CallSheet, DailyProductionReport, CrewCheckIn

@admin.register(CallSheet)
class CallSheetAdmin(admin.ModelAdmin):
    list_display = ('date', 'production', 'published')
    list_filter = ('published', 'production')
    search_fields = ('production__title',)

@admin.register(DailyProductionReport)
class DailyProductionReportAdmin(admin.ModelAdmin):
    list_display = ('dpr_date', 'production')
    list_filter = ('production',)

@admin.register(CrewCheckIn)
class CrewCheckInAdmin(admin.ModelAdmin):
    list_display = ('crew_member', 'call_sheet', 'check_in_time')
    list_filter = ('call_sheet',)
