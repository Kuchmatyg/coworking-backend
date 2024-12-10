from rest_framework import serializers
from .models import Classroom, Booking


class ClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = ['id', 'name', 'description', 'capacity',]


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        nodel = Booking
        fields = ['id', 'classroom', 'user', 'from_date', 'to_date']

class BookingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['classroom', 'user', 'from_time', 'to_time']

    def validate(self, data):
        from_time = data.get('from_time')
        to_time = data.get('to_time')
        classroom = data.get('classroom')

        if from_time >= to_time:
            raise serializers.ValidationError("The 'from_time' must be earlier than 'to_time'.")

        overlapping_bookings = Booking.objects.filter(
            classroom=classroom,
            to_time__gt=from_time,
            from_time__lt=to_time
        )

        if overlapping_bookings.exists():
            raise serializers.ValidationError("This classroom is already booked for the selected time.")

        return data