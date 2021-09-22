from rest_framework import serializers


class LoginRequestSerializer(serializers.Serializer):
    phoneNumber = serializers.CharField()
    password = serializers.CharField()


class SignupRequestSerializer(serializers.Serializer):
    phoneNumber = serializers.CharField()
    password = serializers.CharField()
    firstName = serializers.CharField()
    lastName = serializers.CharField()
