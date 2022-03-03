from rest_framework import serializers
from backend.itrabaho import models, serializers as itrabahoSerializers
from backend.itrabaho.choices import UserTypeChoices


class GetActivityResponseSerializer(itrabahoSerializers.base.ActivityModelSerializer):
    class ContentObjectSerializer(serializers.RelatedField):
        class AcceptedActivitySerializer(
            itrabahoSerializers.base.JobPostModelSerializer
        ):
            recruit = itrabahoSerializers.base.ApplicantsModelSerializer(
                source="applicantId"
            )
            recruiter = itrabahoSerializers.base.RecruiterModelSerializer(
                source="recruiterId"
            )
            applicantReviewId = itrabahoSerializers.base.ReviewModelSerializer()
            recruiterReviewId = itrabahoSerializers.base.ReviewModelSerializer()

            class Meta:
                model = itrabahoSerializers.base.JobPostModelSerializer.Meta.model
                fields = [
                    "street",
                    "barangay",
                    "city",
                    "province",
                    "description",
                    "role",
                    "title",
                    "recruit",
                    "recruiter",
                    "applicantReviewId",
                    "recruiterReviewId",
                    "status",
                    "datetimeCreated",
                ]

        class ReviewActivitySerializer(itrabahoSerializers.base.ReviewModelSerializer):
            jobPost = serializers.SerializerMethodField()
            toUser = itrabahoSerializers.base.UserModelSerializer(source="toUserId")
            fromUser = itrabahoSerializers.base.UserModelSerializer(source="fromUserId")

            class Meta:
                model = itrabahoSerializers.base.ReviewModelSerializer.Meta.model
                fields = ["rate", "comment", "toUser", "fromUser", "jobPost"]

            def get_jobPost(self, reviewInstance):
                # TODO: finish
                # fromUserType = self.context.get("fromUserType")
                fromUserType = UserTypeChoices.RECRUITER

                job = None
                if fromUserType == UserTypeChoices.RECRUITER:
                    job = models.JobPostModel.objects.filter(
                        recruiterReviewId=reviewInstance
                    ).first()
                else:
                    job = models.JobPostModel.objects.filter(
                        applicantReviewId=reviewInstance
                    ).first()

                return itrabahoSerializers.base.JobPostModelSerializer(job).data

        class MatchActivitySerializer(itrabahoSerializers.base.MatchModelSerializer):
            jobPostId = itrabahoSerializers.base.JobPostModelSerializer()
            applicantId = itrabahoSerializers.base.ApplicantsModelSerializer()

            class Meta:
                model = itrabahoSerializers.base.MatchModelSerializer.Meta.model
                fields = ["jobPostId", "applicantId", "score", "rank"]

        def to_representation(self, value):
            if isinstance(value, models.JobPostModel):
                serializer = self.AcceptedActivitySerializer(value)
            elif isinstance(value, models.ReviewModel):
                serializer = self.ReviewActivitySerializer(value)
            elif isinstance(value, models.MatchModel):
                serializer = self.MatchActivitySerializer(value)
            else:
                raise Exception("Content type given is invalid")

            return serializer.data

    content = ContentObjectSerializer(read_only=True, source="contentObject")

    class Meta:
        model = itrabahoSerializers.base.ActivityModelSerializer.Meta.model
        fields = ["datetimeCreated", "type", "content"]


class ProfileStatsSerializer(serializers.Serializer):
    jobs = serializers.IntegerField()
    rating = serializers.IntegerField()
    reviews = serializers.IntegerField()
