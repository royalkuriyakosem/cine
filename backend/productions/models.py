from django.db import models
from django.conf import settings

class Production(models.Model):
    STATUS_CHOICES = [
        ('pre', 'Pre-production'),
        ('shooting', 'Shooting'),
        ('post', 'Post-production'),
        ('completed', 'Completed'),
    ]
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='productions')

    def __str__(self):
        return self.title

class Scene(models.Model):
    production = models.ForeignKey(Production, on_delete=models.CASCADE, related_name='scenes')
    number = models.PositiveIntegerField()
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    pages = models.DecimalField(max_digits=4, decimal_places=2)
    props = models.JSONField(default=dict, blank=True)
    characters = models.JSONField(default=list, blank=True)
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Scene {self.number}: {self.title}"

class Shot(models.Model):
    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    ]
    scene = models.ForeignKey(Scene, on_delete=models.CASCADE, related_name='shots')
    shot_number = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='shots')
    vfx_required = models.BooleanField(default=False)

    def __str__(self):
        return f"Shot {self.shot_number} (Scene {self.scene.number})"

class BudgetLine(models.Model):
    production = models.ForeignKey(Production, on_delete=models.CASCADE, related_name='budget_lines')
    category = models.CharField(max_length=100)
    estimated_amount = models.DecimalField(max_digits=12, decimal_places=2)
    actual_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    vendor = models.CharField(max_length=255, blank=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.category} - {self.production.title}"
