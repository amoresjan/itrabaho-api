from django.contrib.contenttypes import fields
from rest_framework import serializers
from backend.itrabaho import models


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserModel
        fields = ["id", "last_login", "firstName", "lastName", "phoneNumber"]


class ApplicantsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ApplicantModel
        fields = "__all__"


class LoginRequestSerializer(serializers.Serializer):
    phoneNumber = serializers.CharField()
    password = serializers.CharField()
