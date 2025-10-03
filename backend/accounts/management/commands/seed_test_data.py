from django.core.management.base import BaseCommand
from accounts.models import CustomUser

class Command(BaseCommand):
    help = 'Seed test data for CustomUser roles'

    def handle(self, *args, **options):
        test_users = [
            {'username': 'admin', 'email': 'admin@test.com', 'role': 'ADMIN'},
            {'username': 'producer', 'email': 'producer@test.com', 'role': 'PRODUCER'},
            {'username': 'director', 'email': 'director@test.com', 'role': 'DIRECTOR'},
            {'username': 'crew', 'email': 'crew@test.com', 'role': 'CREW'},
            {'username': 'actor', 'email': 'actor@test.com', 'role': 'ACTOR'},
            {'username': 'finance', 'email': 'finance@test.com', 'role': 'FINANCE_LEGAL'},
        ]
        for user in test_users:
            obj, created = CustomUser.objects.get_or_create(
                username=user['username'],
                defaults={
                    'email': user['email'],
                    'role': user['role'],
                }
            )
            if created:
                obj.set_password('testpass123')
                obj.save()
                self.stdout.write(self.style.SUCCESS(f"Created user: {obj.username} ({obj.role})"))
            else:
                self.stdout.write(self.style.WARNING(f"User already exists: {obj.username} ({obj.role})"))
        self.stdout.write(self.style.SUCCESS('Test data seeding complete.'))
