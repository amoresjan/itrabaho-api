from rest_framework import serializers

from backend.itrabaho import models
from backend.itrabaho.choices import AcademicLevelChoices, UserTypeChoices


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


class RecruiterModelSerializer(serializers.ModelSerializer):
    fullName = serializers.CharField(source="getFullName")

    class Meta:
        model = models.RecruiterModel
        fields = "__all__"


class ExperienceDetailModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ExperienceDetailModel
        fields = ["description"]


class ExperienceModelSerializer(serializers.ModelSerializer):
    details = ExperienceDetailModelSerializer(many=True, read_only=True)

    class Meta:
        model = models.ExperienceModel
        exclude = ["id", "profile"]


class ProfileModelSerializer(serializers.ModelSerializer):
    experiences = ExperienceModelSerializer(many=True, read_only=True)
    highesteducationAttained = serializers.SerializerMethodField()

    class Meta:
        model = models.ProfileModel
        exclude = ["id"]

    def get_highesteducationAttained(self, profile):
        return AcademicLevelChoices(profile.highesteducationAttained).label


class ExtendedApplicantsModelSerializer(ApplicantsModelSerializer):
    profile = ProfileModelSerializer(read_only=True)

    class Meta:
        model = models.ApplicantModel
        fields = "__all__"


class ReviewModelSerializer(serializers.ModelSerializer):
    jobId = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = models.ReviewModel
        fields = "__all__"
        read_only_fields = ["fromUserId", "toUserId"]

    def create(self, validated_data):
        jobId = validated_data.pop("jobId")
        job = models.JobPostModel.objects.get(id=jobId)

        fromUserType = self.context.get("fromUserType")
        reviewInstance = None

        if fromUserType == UserTypeChoices.RECRUITER:
            reviewInstance = super().create(
                {
                    **validated_data,
                    "fromUserId": job.recruiterId,
                    "toUserId": job.applicantId,
                }
            )
            job.recruiterReviewId = reviewInstance
            job.save()

        return reviewInstance


class JobPostModelSerializer(serializers.ModelSerializer):
    recruiter = RecruiterModelSerializer(read_only=True, source="recruiterId")
    recruit = ApplicantsModelSerializer(read_only=True, source="applicantId")
    applicantReview = ReviewModelSerializer(read_only=True, source="applicantReviewId")
    recruiterReview = ReviewModelSerializer(read_only=True, source="recruiterReviewId")

    class Meta:
        model = models.JobPostModel
        fields = "__all__"


class ActivityModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ActivityModel
        fields = "__all__"


class MatchModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MatchModel
        fields = "__all__"
