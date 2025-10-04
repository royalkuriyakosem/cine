from django.db import models
from productions.models import Production
from django.conf import settings

class Invoice(models.Model):
    production = models.ForeignKey(Production, on_delete=models.CASCADE, related_name='invoices')
    vendor = models.CharField(max_length=255)
    line_items = models.JSONField(default=list, help_text="List of items, e.g., [{'item': 'Camera Rental', 'cost': 500}]")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    due_date = models.DateField()
    paid = models.BooleanField(default=False)
    uploaded_invoice = models.FileField(upload_to='finance/invoices/', blank=True, null=True)

    def __str__(self):
        return f"Invoice from {self.vendor} for {self.production.title}"

class Contract(models.Model):
    production = models.ForeignKey(Production, on_delete=models.CASCADE, related_name='contracts')
    party_name = models.CharField(max_length=255, help_text="Name of the person or company the contract is with.")
    start_date = models.DateField()
    end_date = models.DateField()
    file = models.FileField(upload_to='finance/contracts/')
    rights = models.JSONField(default=dict, blank=True, help_text="Details about rights, e.g., {'territory': 'Worldwide', 'term': 'Perpetuity'}")
    expiry_alert_sent = models.BooleanField(default=False)

    def __str__(self):
        return f"Contract with {self.party_name} for {self.production.title}"
