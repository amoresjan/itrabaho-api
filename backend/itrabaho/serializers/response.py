from rest_framework import serializers
from backend.itrabaho import models, serializers as itrabahoSerializers


class GetActivityResponseSerializer(itrabahoSerializers.base.ActivityModelSerializer):
    class ContentObjectSerializer(serializers.RelatedField):
        class AcceptedActivitySerializer(
            itrabahoSerializers.base.JobPostModelSerializer
        ):
            applicantId = itrabahoSerializers.base.ApplicantsModelSerializer()
            recruiterId = itrabahoSerializers.base.RecruiterModelSerializer()
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
                    "applicantId",
                    "recruiterId",
                    "applicantReviewId",
                    "recruiterReviewId",
                    "status",
                    "datetimeCreated",
                ]

        class ReviewActivitySerializer(itrabahoSerializers.base.ReviewModelSerializer):
            jobPost = itrabahoSerializers.base.JobPostModelSerializer(source="job")
            toUserId = itrabahoSerializers.base.UserModelSerializer()
            fromUserId = itrabahoSerializers.base.UserModelSerializer()

            class Meta:
                model = itrabahoSerializers.base.ReviewModelSerializer.Meta.model
                fields = ["rate", "comment", "toUserId", "fromUserId", "jobPost"]

        class MatchActivitySerializer(itrabahoSerializers.base.MatchModelSerializer):
            jobPostId = itrabahoSerializers.base.JobPostModelSerializer()
            applicantId = itrabahoSerializers.base.ApplicantsModelSerializer()

            class Meta:
                model = itrabahoSerializers.base.MatchModelSerializer.Meta.model
                fields = ["jobPostId", "applicantId", "percentage", "rank"]

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
