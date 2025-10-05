import random
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from django.db import transaction
from accounts.models import CustomUser
from productions.models import Production, Scene, Shot, BudgetLine, ScriptBreakdown
from scheduling.models import CallSheet, CrewCheckIn
from finance.models import Invoice, Contract
from vfx.models import VFXShot

class Command(BaseCommand):
    help = "Seeds the database with comprehensive dummy data for the entire project."

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write("Starting database seeding...")

        # 0. Ensure default users exist
        if not CustomUser.objects.exists():
            self.stdout.write(self.style.WARNING("No users found. Please run 'create_default_roles' first."))
            return
        
        # 1. Get User References
        producer = CustomUser.objects.filter(role='PRODUCER').first()
        director = CustomUser.objects.filter(role='DIRECTOR').first()
        crew1 = CustomUser.objects.filter(role='CREW').first()
        crew2 = CustomUser.objects.filter(username='upm_ad').first()
        
        if not all([producer, director, crew1, crew2]):
            self.stdout.write(self.style.ERROR("Could not find all required user roles. Make sure default roles are created."))
            return

        # 2. Create Productions
        prod1, created1 = Production.objects.get_or_create(
            title="Project Starlight",
            defaults={
                'slug': 'project-starlight',
                'description': 'A sci-fi epic about interstellar travel.',
                'start_date': date.today() - timedelta(days=30),
                'end_date': date.today() + timedelta(days=60),
                'status': 'shooting',
                'owner': producer
            }
        )
        if created1: self.stdout.write(self.style.SUCCESS(f"Created Production: {prod1.title}"))

        prod2, created2 = Production.objects.get_or_create(
            title="Echoes of Yesterday",
            defaults={
                'slug': 'echoes-of-yesterday',
                'description': 'A historical drama set in the 1920s.',
                'start_date': date.today() + timedelta(days=90),
                'status': 'pre',
                'owner': producer
            }
        )
        if created2: self.stdout.write(self.style.SUCCESS(f"Created Production: {prod2.title}"))

        # 3. Populate Production 1 ("Project Starlight")
        self.populate_production(prod1, director, crew1, crew2)

        self.stdout.write(self.style.SUCCESS("Database seeding complete."))

    def populate_production(self, production, director, crew1, crew2):
        # Script Breakdown
        breakdown, created = ScriptBreakdown.objects.get_or_create(
            production=production,
            defaults={
                'characters': ['CAPTAIN EVA', 'COMMANDER JAX', 'PILOT ZARA'],
                'props': ['Laser Pistol', 'Navigation Console', 'Cryo-pod'],
                'locations': ['Bridge of the Odyssey', 'Engine Room', 'Planet X Surface'],
                'stunts': ['Zero-gravity fight scene'],
                'special_effects': ['Warp drive activation', 'Holographic display']
            }
        )
        if created: self.stdout.write(f"  - Created Script Breakdown for {production.title}")

        # Budget Lines
        budget_lines_data = [
            {'category': 'VFX', 'estimated_amount': 150000, 'actual_amount': 125000, 'vendor': 'Pixel Wizards Inc.', 'approved': True},
            {'category': 'Catering', 'estimated_amount': 25000, 'actual_amount': 28000, 'vendor': 'StarBites Catering', 'approved': True},
            {'category': 'Location Fees', 'estimated_amount': 50000, 'vendor': 'Desert Film Commission', 'approved': False},
        ]
        for data in budget_lines_data:
            BudgetLine.objects.get_or_create(production=production, category=data['category'], defaults=data)
        self.stdout.write(f"  - Created Budget Lines for {production.title}")

        # Scenes and Shots
        scene1, created = Scene.objects.get_or_create(
            production=production, number=1,
            defaults={'title': 'The Bridge', 'location': 'INT. ODYSSEY BRIDGE - DAY', 'pages': 2.5, 'estimated_cost': 12000}
        )
        if created:
            shot1, _ = Shot.objects.get_or_create(scene=scene1, shot_number=1, defaults={'description': 'Wide shot of the crew at their stations.', 'status': 'done', 'assigned_to': director})
            shot2, _ = Shot.objects.get_or_create(scene=scene1, shot_number=2, defaults={'description': 'Close up on Captain Eva.', 'status': 'in_progress', 'vfx_required': True})
            VFXShot.objects.get_or_create(shot=shot2, defaults={'production': production, 'scene': scene1, 'status': 'in_progress', 'assigned_team': 'Internal'})
            self.stdout.write(f"  - Created Scene 1 with shots for {production.title}")

        scene2, created = Scene.objects.get_or_create(
            production=production, number=2,
            defaults={'title': 'Engine Trouble', 'location': 'INT. ENGINE ROOM - DAY', 'pages': 4, 'estimated_cost': 25000}
        )
        if created:
            Shot.objects.get_or_create(scene=scene2, shot_number=1, defaults={'description': 'Sparks fly from a console.', 'status': 'todo', 'vfx_required': True})
            self.stdout.write(f"  - Created Scene 2 with shots for {production.title}")

        # Scheduling
        call_sheet, created = CallSheet.objects.get_or_create(
            production=production, date=date.today(),
            defaults={
                'scenes': [1, 2],
                'crew_assignments': {
                    str(director.id): {'call_time': '08:00', 'role': 'Director'},
                    str(crew1.id): {'call_time': '08:30', 'role': 'Grip'},
                    str(crew2.id): {'call_time': '07:30', 'role': '1st AD'},
                },
                'locations': [{'name': 'Studio A', 'address': '123 Film Way'}],
                'published': True
            }
        )
        if created:
            CrewCheckIn.objects.create(call_sheet=call_sheet, crew_member=director)
            self.stdout.write(f"  - Created Call Sheet and Check-in for {production.title}")

        # Finance
        Invoice.objects.get_or_create(
            production=production, vendor='Pixel Wizards Inc.',
            defaults={'amount': 75000, 'due_date': date.today() + timedelta(days=30), 'paid': False}
        )
        Contract.objects.get_or_create(
            production=production, party_name='Main Actor Agreement',
            defaults={'start_date': date.today() - timedelta(days=30), 'end_date': date.today() + timedelta(days=60)}
        )
        self.stdout.write(f"  - Created Finance records for {production.title}")
