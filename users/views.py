from django.shortcuts import render
#from pycparser.ply.yacc import token
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
import time

from users.models import CustomUser
from users.serializers import LoginSerializer, CustomUserSerializer, RegistrationSerializer


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']

        try:
            user: CustomUser = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({'message': 'Неверный адрес электронной почты или пароль'},
                            status=status.HTTP_401_UNAUTHORIZED)

        if not user.check_password(serializer.validated_data['password']):
            return Response({'message': 'Неверный адрес электронной почты или пароль'},
                            status=status.HTTP_401_UNAUTHORIZED)

        tokens = user.get_token()

        user_serializer = CustomUserSerializer(user)

        return Response({
            "user": user_serializer.data,
            "tokens": tokens
        },
            status=status.HTTP_200_OK)


class RegistrationView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]

    def post(self, request):
        start_time = time.time()
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        group = serializer.validated_data['group']

        if CustomUser.objects.filter(email=email).exists():
            return Response(
                {'message': 'Адрес электронной почты уже зарегистрирован'},
                status=status.HTTP_406_NOT_ACCEPTABLE)

        user = CustomUser.objects.create_user(
            email=email,
            password=password,
            group = group,

        )

        return Response({"message": "Успешная регистрация"},
                        status=status.HTTP_200_OK)

