from django.db.models import query
from rest_framework import response
from backend.itrabaho import models, serializers
from django.contrib.auth import authenticate
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.serializers import Serializer
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.settings import api_settings

# Create your views here.


class LoginController(viewsets.GenericViewSet):
    serializer_class = serializers.base.UserModelSerializer
    queryset = models.UserModel.objects

    @swagger_auto_schema(
        request_body=serializers.request.LoginRequestSerializer(),
        responses={
            200: serializers.base.UserModelSerializer,
            400: "`string`",
        },
    )
    @action(methods=["POST"], detail=False)
    def login(self, request):
        serializer = serializers.request.LoginRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phoneNumber = self.getRequestData(serializer, "phoneNumber")
        password = self.getRequestData(serializer, "password")

        if user := authenticate(username=phoneNumber, password=password):
            self.updateLastLogin(user)
            return self.sendUserResponseData(user)

        return Response("Login unauthorized", status=status.HTTP_401_UNAUTHORIZED)

    def isLGURep(self, user):
        return isinstance(user, models.LGURepresentativeModel)

    def updateLastLogin(self, user):
        user.lastLogin = timezone.now()
        user.save(update_fields=["last_login"])

    def isRecruiter(self, user):
        return isinstance(user, models.RecruiterModel)

    def getRequestData(self, serializer, data):
        return serializer.validated_data.get(data)

    def sendUserResponseData(self, user):
        return Response(self.get_serializer(user).data)

    def checkUserExist(self, phoneNumber):
        return models.UserModel.objects.filter(phoneNumber=phoneNumber)


class ApplicantController(viewsets.GenericViewSet):
    serializer_class = serializers.base.ApplicantsModelSerializer
    queryset = models.ApplicantModel.objects

    def get_queryset(self):
        serializer = serializers.query.ApplicantQuerySerializer(
            data=self.request.query_params
        )

        queryset = self.queryset
        if not serializer.is_valid(raise_exception=True):
            return queryset.all()

        if status := serializer.validated_data.get("status"):
            queryset = queryset.filter(status=status)

        if LGURepresentativeId := serializer.validated_data.get("lguId"):
            queryset = queryset.filter(LGURepresentativeId=LGURepresentativeId)

        return queryset.all()

    def getRequestData(self, serializer, data):
        return serializer.validated_data.get(data)

    def sendUserResponseData(self, applicant):
        return Response(self.get_serializer(applicant).data)

    @swagger_auto_schema(
        responses={
            200: serializers.base.ApplicantsModelSerializer(),
        },
    )
    @action(url_path="get_applicant", methods=["GET"], detail=True)
    def getApplicantById(self, request, *args, **kwargs):
        return self.sendUserResponseData(self.get_object())

    @swagger_auto_schema(
        responses={
            200: serializers.base.ApplicantsModelSerializer(many=True),
        }
    )
    @action(url_path="list_applicants", methods=["GET"], detail=False)
    def getApplicants(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
