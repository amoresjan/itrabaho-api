from rest_framework import serializers

from backend.itrabaho import models


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserModel
        fields = [
            "id",
            "last_login",
            "firstName",
            "lastName",
            "phoneNumber",
            "userType",
        ]


class ApplicantsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ApplicantModel
        fields = [
            "id",
            "last_login",
            "firstName",
            "lastName",
            "phoneNumber",
            "userType",
        ]


class JobPostModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.JobPostModel
        fields = [
            "id",
            "last_login",
            "firstName",
            "lastName",
            "phoneNumber",
            "userType",
        ]


class RecruiterModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RecruiterModel
        fields = [
            "id",
            "last_login",
            "firstName",
            "lastName",
            "phoneNumber",
            "userType",
        ]


class ReviewModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ReviewModel
        fields = [
            "id",
            "last_login",
            "firstName",
            "lastName",
            "phoneNumber",
            "userType",
        ]
