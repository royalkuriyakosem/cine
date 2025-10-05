from django.core.management.base import BaseCommand
from productions.models import Production
from django.utils import timezone

class Command(BaseCommand):
    help = 'Creates test data for the application'

    def handle(self, *args, **kwargs):
        # Create test productions
        productions = [
            {
                'title': 'The Lost City',
                'description': 'An adventure film about a hidden civilization',
                'start_date': timezone.now(),
                'end_date': timezone.now() + timezone.timedelta(days=30),
                'estimated_budget': 1000000.00,
                'status': 'PRE_PRODUCTION'
            },
            {
                'title': 'Midnight Mystery',
                'description': 'A noir detective story',
                'start_date': timezone.now() + timezone.timedelta(days=15),
                'end_date': timezone.now() + timezone.timedelta(days=45),
                'estimated_budget': 500000.00,
                'status': 'DEVELOPMENT'
            }
        ]

        for prod_data in productions:
            Production.objects.create(**prod_data)
            self.stdout.write(self.style.SUCCESS(f'Created production "{prod_data["title"]}"'))