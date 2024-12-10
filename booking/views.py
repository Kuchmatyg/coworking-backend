from rest_framework import generics, permissions
from .models import Classroom, Booking
from .serializers import ClassroomSerializer, BookingSerializer, BookingCreateSerializer


class BookingListView(generics.ListAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


class BookingCreateView(generics.CreateAPIView):
    serializer_class = BookingCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    
