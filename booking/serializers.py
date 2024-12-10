from rest_framework import serializers
from .models import Classroom, Booking


class ClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = ['id', 'name', 'description', 'capacity', ]


class BookingSerializer(serializers.ModelSerializer):
    date = serializers.DateField(format="%d.%m.%Y", input_formats=["%d.%m.%Y"])
    classroom = ClassroomSerializer()

    class Meta:
        model = Booking
        fields = ['id', 'classroom', 'user', 'date', 'from_time', 'to_time', 'created_at', 'updated_at']


class BookingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['classroom', 'user', 'date', 'from_time', 'to_time']

    def validate(self, data):
        date = data.get('date')
        from_time = data.get('from_time')
        to_time = data.get('to_time')
        classroom = data.get('classroom')

        # Validate the time ranges
        if not (8 <= from_time <= 19):
            raise serializers.ValidationError("The 'from_time' must be between 8 and 19.")

        if not (9 <= to_time <= 20):
            raise serializers.ValidationError("The 'to_time' must be between 9 and 20.")

        if from_time >= to_time:
            raise serializers.ValidationError("The 'from_time' must be earlier than 'to_time'.")

        overlapping_bookings = Booking.objects.filter(
            classroom=classroom,
            date=date,
            to_time__gt=from_time,
            from_time__lt=to_time
        )

        if overlapping_bookings.exists():
            raise serializers.ValidationError("This classroom is already booked for the selected time.")

        return data
