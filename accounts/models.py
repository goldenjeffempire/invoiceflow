from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_ADMIN = "admin"
    ROLE_STANDARD = "standard"
    ROLE_CHOICES = (
        (ROLE_ADMIN, "Admin"),
        (ROLE_STANDARD, "Standard User"),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_STANDARD)

    def is_admin(self):
        return self.is_superuser or self.is_staff or self.role == self.ROLE_ADMIN
