from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .exceptions import UserDataException
from users.serializers import UserSerializer
from .sign_up_token import account_activation_token

from users.permissions import AdminPermission, UserPermission


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def signup(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_active = False
            user.save()
            mail_subject = 'confirmation_code has been sent to your email id'
            message = (
                f"'user': '{user}'\n"
                f"'activation_code': "
                f"'{account_activation_token.make_token(user)}'"
            )
            to_email = serializer.initial_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return Response({'username': user.username,
                             'email': user.email},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def user_activation(request):
    if request.method == 'POST':
        try:
            context = {}
            data = request.data
            username = data.get('username')
            activation_token = data.get('confirmation_code')
            if username is None:
                context.update({'username': ["Обязательное поле."]})
            if activation_token is None:
                context.update({'confirmation_code': ["Обязательное поле."]})
            if context:
                raise UserDataException(context)
        except UserDataException as u:
            return Response(u.message, status=status.HTTP_400_BAD_REQUEST)
        user = get_object_or_404(User, username=username)

        if user.is_active:
            return Response({'errors': 'Пользователь уже активирован'},
                            status=status.HTTP_400_BAD_REQUEST)
        if account_activation_token.check_token(user, activation_token):
            user.is_active = True
            user.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'errors': 'неверный confirmation_code'},
                            status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@permission_classes([UserPermission, AdminPermission])
def deactivate(request):
    return Response({'mess': f'all ok {request.user}'})
