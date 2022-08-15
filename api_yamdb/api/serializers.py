from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True,
                                   allow_blank=False,
                                   validators=[
                                       UniqueValidator(
                                           queryset=User.objects.all(),
                                           message='Пользователь с таким '
                                                   'email уже существует!')])

    class Meta:
        model = User
        fields = ('username', 'email')
