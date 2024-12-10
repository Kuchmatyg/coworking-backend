from django.urls import path
from django.contrib import admin

from users.views import LoginView, RegistrationView


urlpatterns = [

    path('login', LoginView.as_view(), name='login'),
    path('registration', RegistrationView.as_view(), name='registration'),
]