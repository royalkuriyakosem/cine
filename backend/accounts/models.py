from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('ADMIN', 'Admin'),
        ('PRODUCER', 'Producer'),
        ('LINE_PRODUCER', 'Line Producer'),
        ('DIRECTOR', 'Director'),
        ('DEPT_HEAD', 'Department Head'),
        ('UPM_AD', 'UPM/AD'),
        ('CREW', 'Crew'),
        ('POST_PROD', 'Post Production'),
        ('FINANCE_LEGAL', 'Finance/Legal'),
        ('ACTOR', 'Actor'),
        ('VENDOR', 'Vendor'),
        ('OBSERVER', 'Observer'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.username} ({self.role})"
