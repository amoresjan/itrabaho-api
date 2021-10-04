from django.contrib.auth import authenticate
from django.db.models import query
from django.http.response import HttpResponse
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.settings import api_settings

from backend.itrabaho import models, serializers

from twilio.twiml.messaging_response import MessagingResponse


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

    @action(
        url_path="sms",
        methods=["POST"],
        detail=False,
    )
    def incoming_sms(self, request):
        """Send a dynamic reply to an incoming text message"""
        # Get the message the user sent our Twilio number
        body = request.data

        # Start our TwiML response
        resp = MessagingResponse()

        # Determine the right reply for this message
        if body["Body"] == "hello":
            resp.message("Hi!")
        elif body["Body"] == "bye":
            resp.message("Goodbye")

        return HttpResponse(str(resp))


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
    @action(url_path="get", methods=["GET"], detail=True)
    def getApplicantById(self, request, *args, **kwargs):
        return self.sendUserResponseData(self.get_object())

    @swagger_auto_schema(
        responses={
            200: serializers.base.ApplicantsModelSerializer(many=True),
        }
    )
    @action(url_path="list", methods=["GET"], detail=False)
    def getApplicants(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class JobPostController(
    viewsets.GenericViewSet,
):
    serializer_class = serializers.base.JobPostModelSerializer
    queryset = models.JobPostModel.objects

    def get_queryset(self):
        serializer = serializers.query.JobPostQuerySerializer(
            data=self.request.query_params
        )

        queryset = self.queryset
        if not serializer.is_valid(raise_exception=True):
            return queryset.all()

        if street := serializer.validated_data.get("street"):
            queryset = queryset.filter(street=street)

        if barangay := serializer.validated_data.get("barangay"):
            queryset = queryset.filter(barangay=barangay)

        if city := serializer.validated_data.get("city"):
            queryset = queryset.filter(city=city)

        if province := serializer.validated_data.get("province"):
            queryset = queryset.filter(province=province)

        if status := serializer.validated_data.get("status"):
            queryset = queryset.filter(status=status)

        if description := serializer.validated_data.get("description"):
            queryset = queryset.filter(description=description)

        if role := serializer.validated_data.get("role"):
            queryset = queryset.filter(role=role)

        if title := serializer.validated_data.get("title"):
            queryset = queryset.filter(title=title)

        if recruiter := serializer.validated_data.get("recruiter"):
            queryset = queryset.filter(recuiterId=recruiter)

        return queryset.all()

    def getRequestData(self, serializer, data):
        return serializer.validated_data.get(data)

    def sendUserResponseData(self, applicant):
        return Response(self.get_serializer(applicant).data)

    @action(url_path="create", methods=["POST"], detail=False)
    def postJob(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        try:
            headers = {"Location": str(serializer.data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            headers = {}
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    @action(url_path="recruiter", methods=["GET"], detail=True)
    def getJobPostsByRecruiter(self, request, pk=None):
        queryset = models.JobPostModel.objects.filter(recruiterId=pk)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        responses={
            200: serializers.base.JobPostModelSerializer(many=True),
        }
    )
    @action(url_path="list", methods=["GET"], detail=False)
    def getJobPosts(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        responses={
            200: serializers.base.JobPostModelSerializer(),
        },
    )
    @action(url_path="get", methods=["GET"], detail=True)
    def getJobPostById(self, request, *args, **kwargs):
        return self.sendUserResponseData(self.get_object())


class SignUpController(viewsets.GenericViewSet):
    serializer_class = serializers.base.UserModelSerializer
    queryset = models.UserModel.objects

    def getRequestData(self, serializer, data):
        return serializer.validated_data.get(data)

    def sendUserResponseData(self, user):
        return Response(self.get_serializer(user).data)

    @swagger_auto_schema(
        responses={200: serializers.base.UserModelSerializer(), 401: "`string`"},
    )
    @action(url_path="signup", methods=["POST"], detail=False)
    def signup(self, request):
        serializer = serializers.request.SignupRequestSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        phoneNumber = self.getRequestData(serializer, "phoneNumber")
        password = self.getRequestData(serializer, "password")
        firstName = self.getRequestData(serializer, "firstName")
        lastName = self.getRequestData(serializer, "lastName")

        if self.checkMobileNumberExist(phoneNumber):
            return Response(
                "Phone number is already taken",
                status=status.HTTP_401_UNAUTHORIZED,
            )

        user = models.UserModel.objects.create_user(
            phoneNumber=phoneNumber,
            password=password,
            firstName=firstName,
            lastName=lastName,
        )

        return self.sendUserResponseData(user)

    def checkMobileNumberExist(self, phoneNumber):
        return models.UserModel.objects.filter(phoneNumber=phoneNumber).exists()


class RecruiterController(viewsets.GenericViewSet):
    serializer_class = serializers.base.RecruiterModelSerializer
    queryset = models.RecruiterModel.objects

    def getRequestData(self, serializer, data):
        return serializer.validated_data.get(data)

    def sendUserResponseData(self, user):
        return Response(self.get_serializer(user).data)

    @swagger_auto_schema(
        responses={
            200: serializers.base.RecruiterModelSerializer(),
        },
    )
    @action(url_path="get", methods=["GET"], detail=True)
    def getRecruiterById(self, request, *args, **kwargs):
        return self.sendUserResponseData(self.get_object())

    @action(url_path="jobs", methods=["GET"], detail=True)
    def getJobPosts(self, request, pk):
        queryset = models.JobPostModel.objects.filter(recruiterId=pk)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = serializers.base.JobPostModelSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = serializers.base.JobPostModelSerializer(queryset, many=True)
        return Response(serializer.data)


class ReviewController(viewsets.GenericViewSet):
    serializer_class = serializers.base.ReviewModelSerializer
    queryset = models.ReviewModel.objects

    @swagger_auto_schema(responses={200: serializers.base.ReviewModelSerializer()})
    @action(url_path="review", methods=["POST"], detail=False)
    def postReview(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        try:
            headers = {"Location": str(serializer.data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            headers = {}
        return self.sendReviewResponseData(serializer, headers)

    def sendReviewResponseData(self, serializer, headers):
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
