from rest_framework import serializers

from backend.itrabaho import models


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserModel
        fields = ["id", "last_login", "firstName", "lastName", "phoneNumber"]


class ApplicantsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ApplicantModel
        fields = ["id", "last_login", "firstName", "lastName", "phoneNumber"]


class JobPostModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.JobPostModel
        fields = "__all__"


class RecruiterModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RecruiterModel
        fields = ["id", "last_login", "firstName", "lastName", "phoneNumber"]


class ReviewModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ReviewModel
        fields = "__all__"
