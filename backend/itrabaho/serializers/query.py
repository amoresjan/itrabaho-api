from rest_framework import serializers
from backend.itrabaho import models


class ApplicantQuerySerializer(serializers.Serializer):
    status = serializers.CharField(required=False)
    LGURepresentative = serializers.IntegerField(required=False)
