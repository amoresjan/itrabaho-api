from rest_framework import serializers


class LoginRequestSerializer(serializers.Serializer):
    phoneNumber = serializers.CharField()
    password = serializers.CharField()
