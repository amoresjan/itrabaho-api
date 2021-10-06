from rest_framework import serializers

from backend.itrabaho import models


class UserModelSerializer(serializers.ModelSerializer):
    fullName = serializers.CharField(source="getFullName")

    class Meta:
        model = models.UserModel
        fields = "__all__"


class ApplicantsModelSerializer(serializers.ModelSerializer):
    fullName = serializers.CharField(source="getFullName")

    class Meta:
        model = models.ApplicantModel
        fields = "__all__"


class JobPostModelSerializer(serializers.ModelSerializer):
    recruiterId = UserModelSerializer()

    class Meta:
        model = models.JobPostModel
        fields = "__all__"


class RecruiterModelSerializer(serializers.ModelSerializer):
    fullName = serializers.CharField(source="getFullName")

    class Meta:
        model = models.RecruiterModel
        fields = "__all__"


class ReviewModelSerializer(serializers.ModelSerializer):
    fromUser = UserModelSerializer()
    toUser = UserModelSerializer()

    class Meta:
        model = models.ReviewModel
        fields = "__all__"


class ActivityModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ActivityModel
        fields = "__all__"


class MatchModelSerializer(serializers.ModelSerializer):
    jobPostId = JobPostModelSerializer()
    applicantId = ApplicantsModelSerializer()

    class Meta:
        model = models.MatchModel
        fields = "__all__"
