from backend.itrabaho import models
from rest_framework import serializers


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserModel
        fields = ["id", "last_login", "firstName", "lastName", "phoneNumber"]


class ApplicantsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ApplicantModel
        fields = ["id", "last_login", "firstName", "lastName", "phoneNumber"]
