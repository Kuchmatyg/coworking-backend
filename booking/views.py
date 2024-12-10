from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Classroom
from .serializers import ClassroomSerializer


# Доступ для всех пользователей (только просмотр)
class ClassroomListView(generics.ListCreateAPIView):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]
    
# Доступ к конкретому помещению
class ClassroomDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE']:
            return [permissions.IsAdminUser]
        return [permissions.AllowAny()]
    
    
