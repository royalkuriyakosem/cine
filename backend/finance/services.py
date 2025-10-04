from decimal import Decimal
from django.db.models import Avg, Count
from productions.models import Production

class BudgetPredictionService:
    """
    Service for predicting production budgets based on historical data.
    Currently uses simple heuristics - TODO: Replace with ML model.
    """
    
    def __init__(self, production: Production):
        self.production = production
    
    def predict_budget(self) -> dict:
        """
        Predict total budget and provide category breakdown.
        
        TODO: Replace this heuristic implementation with:
        1. Trained ML model using historical production data
        2. Consider factors like:
           - Genre
           - Script length
           - VFX requirements
           - Location complexity
           - Cast size
           - Shooting schedule
        """
        # Get basic production stats
        total_scenes = self.production.scenes.count()
        vfx_shots = self.production.vfx_shots.count()
        total_pages = sum(scene.pages for scene in self.production.scenes.all())
        
        # Get historical averages
        historical_data = self._get_historical_averages()
        
        # Calculate base prediction using simple multipliers
        base_cost = Decimal('10000.00')  # Base cost per scene
        vfx_cost = Decimal('5000.00')    # Additional cost per VFX shot
        page_cost = Decimal('2000.00')    # Cost per script page
        
        # Calculate category estimates
        categories = {
            'production': base_cost * total_scenes,
            'post_production': vfx_cost * vfx_shots,
            'talent': page_cost * total_pages,
            'equipment': base_cost * (total_scenes / 2),
            'locations': base_cost * (total_scenes / 3),
        }
        
        # Apply historical adjustments if available
        if historical_data['avg_scene_cost']:
            categories['production'] = historical_data['avg_scene_cost'] * total_scenes
        
        predicted_total = sum(categories.values())
        
        return {
            'predicted_total': predicted_total,
            'details': {
                'categories': categories,
                'factors': {
                    'total_scenes': total_scenes,
                    'vfx_shots': vfx_shots,
                    'total_pages': float(total_pages),
                },
                'historical_data': historical_data
            }
        }
    
    def _get_historical_averages(self) -> dict:
        """Get average costs from completed productions"""
        completed_productions = Production.objects.filter(
            status='completed'
        ).exclude(id=self.production.id)
        
        if not completed_productions.exists():
            return {
                'avg_scene_cost': None,
                'avg_total_budget': None,
                'sample_size': 0
            }
        
        # Calculate averages from historical data
        budget_data = completed_productions.aggregate(
            avg_total=Avg('budget_lines__actual_amount'),
            total_scenes=Count('scenes'),
        )
        
        if budget_data['total_scenes'] > 0:
            avg_scene_cost = budget_data['avg_total'] / budget_data['total_scenes']
        else:
            avg_scene_cost = None
            
        return {
            'avg_scene_cost': avg_scene_cost,
            'avg_total_budget': budget_data['avg_total'],
            'sample_size': completed_productions.count()
        }

def generate_budget_prediction(production: Production) -> 'BudgetPrediction':
    """Generate and save a new budget prediction"""
    from .models import BudgetPrediction  # Import here to avoid circular import
    
    predictor = BudgetPredictionService(production)
    prediction = predictor.predict_budget()
    
    return BudgetPrediction.objects.create(
        production=production,
        predicted_total=prediction['predicted_total'],
        details=prediction['details']
    )