from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from backend.itrabaho.choices import UserTypeChoices


class ApplicantQuerySerializer(serializers.Serializer):
    status = serializers.CharField(required=False)
    LGURepresentative = serializers.IntegerField(required=False)
    jobPostId = serializers.IntegerField(required=False)


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


class ActivityQuerySerializer(serializers.Serializer):
    user = serializers.CharField(required=False)


VALID_REVIEW_USER_TYPES = [UserTypeChoices.RECRUITER, UserTypeChoices.APPLICANT]


def validate_user_type(value: str):
    if value not in VALID_REVIEW_USER_TYPES:
        raise ValidationError("User type must be R or A.")


class ReviewContextSerializer(serializers.Serializer):
    fromUserType = serializers.CharField(validators=[validate_user_type])
