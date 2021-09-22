from django.views.decorators.csrf import requires_csrf_token
from rest_framework import serializers
from backend.itrabaho import models


class ApplicantQuerySerializer(serializers.Serializer):
    status = serializers.CharField(required=False)
    LGURepresentative = serializers.IntegerField(required=False)


class JobPostQuerySerializer(serializers.Serializer):
    street = serializers.CharField(required=False)
    barangay = serializers.CharField(required=False)
    city = serializers.CharField(required=False)
    province = serializers.CharField(required=False)
    status = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    role = serializers.CharField(required=False)
    title = serializers.CharField(required=False)
    recruiter = serializers.IntegerField(required=False)
