from django.shortcuts import render

from rest_framework import generics, status
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend

from admins.serializers import GetAllSerializer
from booking.models import Booking, Classroom
from booking.serializers import ClassroomSerializer, BookingSerializer, BookingCreateSerializer
from users.models import CustomUser, Group
from users.serializers import CustomUserSerializer, GroupSerializer
from admins.filters import CustomUserFilter


class GetAllUsersView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]



class CreateGroupView(generics.CreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    # def post(self, request):
    #     serializer = self.serializer_class(data=request.data)

    def perform_create(self, serializer):
        group_name = serializer.validated_data.get('name')
        if Group.objects.filter(name=group_name).exists():
            raise ValidationError({"detail": "Группа с таким именем уже существует."})

        serializer.save()
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreateClassroomView(generics.CreateAPIView):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        classroom_name = serializer.validated_data.get('name')
        if Classroom.objects.filter(name=classroom_name).exists():
            raise ValidationError({"detail": "Кабинет с таким именем уже существует."})
        serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateGroupView(generics.UpdateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    lookup_field = 'id'

class UpdateClassroomView(generics.UpdateAPIView):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    lookup_field = 'id'

class UpdateBookingView(generics.UpdateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    lookup_field = 'id'

class DeleteGroupView(generics.DestroyAPIView):
    queryset = Group.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    lookup_field = 'id'

    def perform_destroy(self, instance):
        instance.delete()

class DeleteClassroomView(generics.DestroyAPIView):
    queryset = Classroom.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    lookup_field = 'id'

    def perform_destroy(self, instance):
        instance.delete()

class DeleteBookingView(generics.DestroyAPIView):
    queryset = Booking.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    lookup_field = 'id'

    def perform_destroy(self, instance):
        instance.delete()


class GetUsersByGroupView(generics.ListAPIView):
    serializer_class = CustomUserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        group_id = self.kwargs['group_id']
        return CustomUser.objects.filter(group__id=group_id)


class FilterUsersView(generics.ListAPIView):
    serializer_class = CustomUserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CustomUserFilter

    def get_queryset(self):
        return CustomUser.objects.all()


class GetAll(generics.ListAPIView):
    serializer_class = GetAllSerializer

    def get_queryset(self):
        users = CustomUser.objects.all()
        groups = Group.objects.all()
        bookings = Booking.objects.all()
        classrooms = Classroom.objects.all()

        return {
            'users': users,
            'groups': groups,
            'booking': bookings,
            'classrooms': classrooms
        }

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        serializer = self.get_serializer(queryset)
        return Response(serializer.data)