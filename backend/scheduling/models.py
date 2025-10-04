from django.db import models
from productions.models import Production
from django.conf import settings

class CallSheet(models.Model):
    production = models.ForeignKey(Production, on_delete=models.CASCADE, related_name='call_sheets')
    date = models.DateField()
    scenes = models.JSONField(default=list, help_text="List of scene numbers to be shot.")
    crew_assignments = models.JSONField(default=dict, help_text="Dict mapping user IDs to their call times and roles for the day.")
    locations = models.JSONField(default=list, help_text="List of locations for the day with addresses and notes.")
    published = models.BooleanField(default=False)

    def __str__(self):
        return f"Call Sheet for {self.production.title} on {self.date}"

class DailyProductionReport(models.Model):
    production = models.ForeignKey(Production, on_delete=models.CASCADE, related_name='dprs')
    dpr_date = models.DateField()
    scenes_completed_list = models.JSONField(default=list, help_text="List of scenes completed.")
    issues = models.JSONField(default=dict, help_text="Notes on issues encountered during the day.")
    expenses = models.JSONField(default=list, help_text="List of expenses incurred.")

    def __str__(self):
        return f"DPR for {self.production.title} on {self.dpr_date}"

class CrewCheckIn(models.Model):
    call_sheet = models.ForeignKey(CallSheet, on_delete=models.CASCADE, related_name='check_ins')
    crew_member = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='check_ins')
    check_in_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('call_sheet', 'crew_member')

    def __str__(self):
        return f"{self.crew_member.username} checked in for {self.call_sheet.date}"
