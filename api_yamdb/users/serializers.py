from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

from users.models import User, ROLES


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True,
                                   allow_blank=False,
                                   validators=[
                                       UniqueValidator(
                                           queryset=User.objects.all(),
                                           message='Пользователь с таким '
                                                   'email уже существует!')])
    role = serializers.ChoiceField(choices=ROLES, default='user')

    def validate_username(self, value):
        if value == 'me':
            raise ValidationError("Не может быть 'me'.")
        return value

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role')
