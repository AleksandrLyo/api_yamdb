from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .auth.sign_up_token import account_activation_token
from .serializers import UserSerializer


@api_view(['POST'])
# @authentication_classes([])
def signup(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_active = False
            user.save()
            mail_subject = 'confirmation_code has been sent to your email id'
            message = (f"'user': {user}\n"
                       f"'activation_code':"
                       f" {account_activation_token.make_token(user)}")
            to_email = serializer.initial_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def activate(request):
    if request.method == 'POST':
        try:
            data = request.data
            print(data)
            user = get_object_or_404(User, username=data.get('username'))
            activation_token = data.get('confirmation_code')
            print(activation_token)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user,
                                                                     activation_token):
            user.is_active = True
            user.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
    return Response(status=status.HTTP_400_BAD_REQUEST)
