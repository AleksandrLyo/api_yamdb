from django.contrib.auth.models import AbstractUser
from django.db import models

ROLES = (
    ('admin', 'администратор'),
    ('moderator', 'модератор'),
    ('user', 'пользователь'),
)


class User(AbstractUser):
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    bio = models.TextField(null=True, blank=True, help_text='О себе')
    role = models.CharField(max_length=20, choices=ROLES, default='user')
    confirmation_code = models.TextField(null=True)

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    @property
    def is_admin(self):
        return self.role == 'admin'

    def __str__(self):
        return str(self.username)
