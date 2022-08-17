from django.contrib.auth.models import User as _User
from django.db import models

# Create your models here.

ROLES = (
    ('admin', 'администратор'),
    ('moderator', 'модератор'),
    ('user', 'пользователь'),
)


class User(_User):
    bio = models.TextField(null=True, blank=True, help_text='О себе')
    role = models.CharField(max_length=20)
