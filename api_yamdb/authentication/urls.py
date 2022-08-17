from django.urls import path

from .views import signup, user_activation, deactivate

app_name = 'authentication'

urlpatterns = [
    path('signup/', signup),
    path('token/', user_activation),
    path('deactivation/', deactivate)
]