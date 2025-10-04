from celery import shared_task
from .models import Production
from .budget import predict_budget_for_production
import logging

logger = logging.getLogger(__name__)

@shared_task
def recalculate_budget_predictions():
    """
    Nightly task to recalculate budget predictions for all active productions.
    """
    active_productions = Production.objects.exclude(status='completed')
    logger.info(f"Starting nightly budget prediction for {active_productions.count()} productions.")
    
    for production in active_productions:
        try:
            predict_budget_for_production(production)
            logger.info(f"Successfully recalculated budget for production: {production.title}")
        except Exception as e:
            logger.error(f"Failed to recalculate budget for {production.title}: {e}")
    
    logger.info("Nightly budget prediction task finished.")