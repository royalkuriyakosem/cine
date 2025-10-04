from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from productions.models import Production
from .services import generate_budget_prediction
from .models import Contract
import logging

logger = logging.getLogger(__name__)

@shared_task
def update_budget_predictions():
    """Update budget predictions for all active productions."""
    active_statuses = ['pre', 'shooting', 'post']
    active_productions = Production.objects.filter(status__in=active_statuses)
    
    results = {
        'total': active_productions.count(),
        'updated': 0,
        'errors': 0
    }
    
    for production in active_productions:
        try:
            generate_budget_prediction(production)
            results['updated'] += 1
        except Exception as e:
            results['errors'] += 1
            print(f"Error updating prediction for {production.title}: {str(e)}")
    
    return f"Updated {results['updated']} predictions ({results['errors']} errors)"

@shared_task
def check_contract_expirations():
    """
    Nightly task to find contracts expiring soon and send an alert.
    """
    alert_days = 30
    upcoming_expiry_date = timezone.now().date() + timedelta(days=alert_days)
    
    expiring_contracts = Contract.objects.filter(
        end_date__lte=upcoming_expiry_date,
        expiry_alert_sent=False
    )
    
    for contract in expiring_contracts:
        logger.info(f"ALERT: Contract '{contract.party_name}' for production '{contract.production.title}' is expiring on {contract.end_date}.")
        contract.expiry_alert_sent = True
        contract.save()
        
    return f"Checked {expiring_contracts.count()} expiring contracts."