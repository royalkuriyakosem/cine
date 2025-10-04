from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from productions.models import Production
from .services import generate_budget_prediction

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