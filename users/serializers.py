from rest_framework import serializers

from users.models import CustomUser, Group


class CustomUserSerializer(serializers.ModelSerializer):
    isAdmin = serializers.BooleanField(source="is_admin")

    class Meta:
        model = CustomUser
        fields = ["id", "email", "name" ,"isAdmin"]

class GrouSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128, write_only=True)


class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    name = serializers.CharField()
    password = serializers.CharField(max_length=128, write_only=True)
    group = serializers.PrimaryKeyRelatedField(many=False, queryset=Group.objects.all(), allow_null=True)

class RefreshTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()


