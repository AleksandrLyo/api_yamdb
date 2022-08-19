from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

ROLES = (
    ('admin', 'администратор'),
    ('moderator', 'модератор'),
    ('user', 'пользователь'),
)

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True,
                                   allow_blank=False,
                                   validators=[
                                       UniqueValidator(
                                           queryset=User.objects.all(),
                                           message='Пользователь с таким '
                                                   'email уже существует!')])
    role = serializers.ChoiceField(choices=ROLES, default='user',
                                   read_only=True)

    def validate_username(self, value):
        if value == 'me':
            raise ValidationError("Не может быть 'me'.")
        return value

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role')


class AdminUserSerializer(UserSerializer):
    role = serializers.ChoiceField(choices=ROLES, default='user')
