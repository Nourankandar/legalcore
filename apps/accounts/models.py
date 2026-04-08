
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ADMIN = 'ADMIN'
    LAWYER = 'LAWYER'
    CLIENT = 'CLIENT'

    ROLE_CHOICES = [
        (ADMIN , 'admin'),
        (LAWYER , 'lawyer'),
        (CLIENT , 'client')
    ]

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=CLIENT
    )

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"