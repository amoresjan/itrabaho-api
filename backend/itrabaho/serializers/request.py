from django.db import transaction
from rest_framework import serializers

from backend.itrabaho.models import (
    ApplicantModel,
    ExperienceDetailModel,
    ExperienceModel,
    ProfileModel,
)


class LoginRequestSerializer(serializers.Serializer):
    phoneNumber = serializers.CharField()
    password = serializers.CharField()


class SignupRequestSerializer(serializers.Serializer):
    phoneNumber = serializers.CharField()
    password = serializers.CharField()
    firstName = serializers.CharField()
    lastName = serializers.CharField()


class CreateApplicantRequestSerializer(serializers.ModelSerializer):
    class ProfileSerializer(serializers.ModelSerializer):
        class ExperienceSerializer(serializers.ModelSerializer):
            class ExperienceDetailSerializer(serializers.ModelSerializer):
                class Meta:
                    model = ExperienceDetailModel
                    fields = ["description"]

            details = serializers.ListField(
                child=ExperienceDetailSerializer(), write_only=True
            )

            class Meta:
                model = ExperienceModel
                exclude = ["id", "profile"]

        experiences = serializers.ListField(
            child=ExperienceSerializer(), write_only=True
        )

        class Meta:
            model = ProfileModel
            fields = ["yearsOfExperience", "highesteducationAttained", "experiences"]

    profile = ProfileSerializer()

    class Meta:
        model = ApplicantModel
        fields = [
            "firstName",
            "lastName",
            "phoneNumber",
            "sex",
            "birthDate",
            "profile",
            "skills",
            "LGURepresentativeId",
        ]

    @transaction.atomic
    def create(self, validated_data):
        profile_data = validated_data.pop("profile")
        experiences_data = profile_data.pop("experiences")
        skills_data = validated_data.pop("skills")

        profile = ProfileModel.objects.create(**profile_data)
        applicant = ApplicantModel.objects.create(**validated_data, profile=profile)
        applicant.skills.set(skills_data)

        for experience in experiences_data:
            details = experience.pop("details")

            experience_instance = ExperienceModel.objects.create(
                **experience, profile=profile
            )

            ExperienceDetailModel.objects.bulk_create(
                [
                    ExperienceDetailModel(
                        experience=experience_instance,
                        description=detail.get("description"),
                    )
                    for detail in details
                ]
            )

        return applicant
