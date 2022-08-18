from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    bio = models.TextField(null=True, blank=True, help_text='О себе')
    role = models.CharField(max_length=150)

    def __str__(self):
        return str(self.username)
