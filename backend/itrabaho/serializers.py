from rest_framework import serializers
from backend.itrabaho import models


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserModel
        fields = ["id", "last_login", "firstName", "lastName", "phoneNumber"]


class LoginRequestSerializer(serializers.Serializer):
    phoneNumber = serializers.CharField()
    password = serializers.CharField()
