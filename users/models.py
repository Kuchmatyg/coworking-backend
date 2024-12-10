import uuid
from tkinter.constants import CASCADE

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from django.db.models import Q


class Group(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )

    name = models.CharField(unique=True, max_length=255)

    def __str__(self):
        return self.name


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, is_admin=False, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_admin', True)

        return self.create_user(email, password, **extra_fields)

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset


class AllUsersManager(BaseUserManager):
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset


class CustomUser(AbstractBaseUser):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )

    email = models.EmailField()
    name = models.CharField(max_length=255)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)
    is_admin = models.BooleanField()

    objects = CustomUserManager()
    all_objects = AllUsersManager()

    def __str__(self):
        return self.email

    def get_token(self):
        access_token = AccessToken.for_user(self)
        refresh_token = RefreshToken.for_user(self)

        return {
            'accessToken': str(access_token),
            'refreshToken': str(refresh_token),
        }

    @property
    def token_payload(self):
        return {
            'id': self.id,
            'email': self.email,
        }
