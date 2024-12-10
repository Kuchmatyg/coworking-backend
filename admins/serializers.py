from rest_framework import serializers

from booking.serializers import BookingSerializer, ClassroomSerializer
from users.models import CustomUser, Group
from users.serializers import CustomUserSerializer, GroupSerializer


class GetAllSerializer(serializers.Serializer):
    users = CustomUserSerializer(many=True)
    groups = GroupSerializer(many=True)
    booking = BookingSerializer(many=True)
    classrooms = ClassroomSerializer(many=True)


