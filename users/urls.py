from django.urls import path
from django.contrib import admin

from users.views import LoginView, RegistrationView, AuthView, CustomTokenRefreshView, GroupList

urlpatterns = [

    path('login', LoginView.as_view(), name='login'),
    path('registration', RegistrationView.as_view(), name='registration'),
    path('auth', AuthView.as_view(), name='auth'),
    path('refresh', CustomTokenRefreshView.as_view(), name='refresh'),
    path('groups', GroupList.as_view(), name='groups'),

]