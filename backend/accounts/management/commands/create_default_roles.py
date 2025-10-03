from django.core.management.base import BaseCommand
from accounts.models import CustomUser

class Command(BaseCommand):
    help = "Create one user for each predefined role"

    def handle(self, *args, **kwargs):
        roles = [choice[0] for choice in CustomUser.ROLE_CHOICES]
        for role in roles:
            username = role.lower()
            if not CustomUser.objects.filter(username=username).exists():
                CustomUser.objects.create_user(
                    username=username,
                    password='password123',
                    role=role,
                    email=f"{username}@example.com"
                )
                self.stdout.write(self.style.SUCCESS(f"Created user: {username} ({role})"))
            else:
                self.stdout.write(f"User {username} already exists.")