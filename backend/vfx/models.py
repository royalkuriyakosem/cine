from django.db import models
from django.conf import settings
from productions.models import Production, Scene, Shot

class VFXShot(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('review', 'In Review'),
        ('approved', 'Approved'),
        ('omitted', 'Omitted'),
    ]
    production = models.ForeignKey(Production, on_delete=models.CASCADE, related_name='vfx_shots')
    scene = models.ForeignKey(Scene, on_delete=models.CASCADE, related_name='vfx_shots')
    shot = models.OneToOneField(Shot, on_delete=models.CASCADE, related_name='vfx_shot')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    assigned_team = models.CharField(max_length=100, blank=True, help_text="Name of the team or vendor.")
    due_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"VFX for Shot {self.shot.shot_number} (Scene {self.scene.number})"

class Asset(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='vfx/assets/')
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    metadata = models.JSONField(default=dict, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ShotVersion(models.Model):
    vfx_shot = models.ForeignKey(VFXShot, on_delete=models.CASCADE, related_name='versions')
    version_number = models.PositiveIntegerField()
    file = models.FileField(upload_to='vfx/versions/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        unique_together = ('vfx_shot', 'version_number')
        ordering = ['-version_number']

    def __str__(self):
        return f"Version {self.version_number} for {self.vfx_shot}"
