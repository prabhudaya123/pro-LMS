from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    phone_no = models.CharField(max_length=15, blank=True, null=True)  # Add phone number
    date_of_birth = models.DateField(blank=True, null=True)  # Add date of birth
