from django.shortcuts import render

from rest_framework import generics, status
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend

from users.models import CustomUser, Group
from admins.serializers import CustomUserSerializer, GroupSerializer
from admins.filters import CustomUserFilter

# Получить список всех пользователей
class GetAllUsersView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]


# Создать группу
class CreateGroupView(generics.CreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]

    # def post(self, request):
    #     serializer = self.serializer_class(data=request.data)

    def perform_create(self, serializer):
        # Проверяем, существует ли уже группа с таким именем
        group_name = serializer.validated_data.get('name')  # доступ к validated_data после валидации
        if Group.objects.filter(name=group_name).exists():
            raise ValidationError({"detail": "Группа с таким именем уже существует."})
        
        # Если группа не существует, сохраняем её
        serializer.save()
    
    def create(self, request, *args, **kwargs):
        # Сначала валидируем данные
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():  # Валидация
            # Если данные валидны, вызываем perform_create
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# Получить всех пользователей, принадлежащих определенной группе.
class GetUsersByGroupView(generics.ListAPIView):
    serializer_class = CustomUserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]

    def get_queryset(self):
        group_id = self.kwargs['group_id']
        return CustomUser.objects.filter(group__id=group_id)

# Фильтрация пользователей по email или имени
class FilterUsersView(generics.ListAPIView):
    """
    Фильтрация пользователей по email или имени.
    """
    serializer_class = CustomUserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CustomUserFilter

    def get_queryset(self):
        # Возвращаем все объекты CustomUser, фильтруемые с помощью фильтра
        return CustomUser.objects.all()
