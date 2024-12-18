from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication

from .filters import BookingFilter
from .serializers import ClassroomSerializer, BookingSerializer, BookingCreateSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Classroom, Booking
from .serializers import BookingSerializer
from django.utils.dateparse import parse_date


class BookingListView(generics.ListAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = BookingFilter


class BookingCreateView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = BookingCreateSerializer


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class GetClassroomBookingsView(APIView):
    def get(self, request, *args, **kwargs):
        day_str = request.GET.get('day', None)

        if not day_str:
            return Response({"detail": "Day parameter is required."}, status=status.HTTP_400_BAD_REQUEST)


        try:
            day = parse_date(day_str)
            if day is None:
                return Response({"detail": "Invalid date format. Please use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({"detail": "Invalid date format. Please use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        classrooms = Classroom.objects.all()

        classroom_booking_data = []

        bookings = Booking.objects.filter(date=day)

        for classroom in classrooms:
            classroom_bookings = bookings.filter(classroom=classroom)

            bookings_data = BookingSerializer(classroom_bookings, many=True).data

            classroom_booking_data.append({
                'id': str(classroom.id),
                'name': classroom.name,
                'bookings': bookings_data
            })

        return Response(classroom_booking_data, status=status.HTTP_200_OK)


class UserBookingsView(generics.ListAPIView):
    serializer_class = BookingSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Booking.objects.filter(user=user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ClassroomsView(generics.ListAPIView):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)