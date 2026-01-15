from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('standard', 'Standard User'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='standard')
    
    def is_admin(self):
        return self.role == 'admin'
