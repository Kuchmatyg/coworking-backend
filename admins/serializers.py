from rest_framework import serializers
from users.models import CustomUser, Group


class CustomUserSerializer(serializers.ModelSerializer):
    isAdmin = serializers.BooleanField(source="is_admin")

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'name', 'group', 'isAdmin']

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'