from decimal import Decimal
from django.db.models import Sum
from .models import Production, BudgetPrediction

def predict_budget_for_production(production: Production) -> BudgetPrediction:
    """
    Predicts budget for a given production using a simple heuristic.
    """
    # Heuristic: Average the actual budget of the last 3 completed productions.
    previous_productions = Production.objects.filter(
        status='completed'
    ).exclude(id=production.id).order_by('-end_date')[:3]

    total_actual_budget = Decimal('0.0')
    count = 0
    details = {
        'reasoning': '',
        'based_on_productions': []
    }

    if previous_productions:
        for p in previous_productions:
            # Sum up actual amounts from budget lines for each production
            actual_budget = p.budget_lines.aggregate(total=Sum('actual_amount'))['total']
            if actual_budget:
                total_actual_budget += actual_budget
                count += 1
                details['based_on_productions'].append({'id': p.id, 'title': p.title, 'budget': float(actual_budget)})
    
    if count > 0:
        predicted_total = total_actual_budget / count
        details['reasoning'] = f"Based on the average budget of the last {count} completed productions."
    else:
        # Fallback: Use the current production's estimated budget or a default.
        estimated_budget = production.budget_lines.aggregate(total=Sum('estimated_amount'))['total']
        if estimated_budget:
            predicted_total = estimated_budget
            details['reasoning'] = "Fallback: Used the sum of estimated budget lines for this production."
        else:
            predicted_total = Decimal('50000.00') # Default estimate
            details['reasoning'] = "Fallback: No historical data or estimated budget found. Used a default value."

    # Create and save the prediction
    prediction = BudgetPrediction.objects.create(
        production=production,
        predicted_total=predicted_total,
        details=details
    )
    return prediction