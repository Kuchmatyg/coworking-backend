from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
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

        bookings = Booking.objects.filter(date=day)

        classrooms = Classroom.objects.all()
        classroom_booking_data = []

        for classroom in classrooms:
            classroom_bookings = bookings.filter(classroom=classroom)
            if classroom_bookings.exists():
                bookings_data = BookingSerializer(classroom_bookings, many=True).data
                classroom_booking_data.append({
                    'id': str(classroom.id),
                    'name': classroom.name,
                    'bookings': bookings_data
                })

        return Response(classroom_booking_data, status=status.HTTP_200_OK)


    

