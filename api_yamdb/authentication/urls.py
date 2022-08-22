from django.urls import path

from .views import signup, user_activation

app_name = 'authentication'

urlpatterns = [
    path('v1/auth/signup/', signup),
    path('v1/auth/token/', user_activation),
]
