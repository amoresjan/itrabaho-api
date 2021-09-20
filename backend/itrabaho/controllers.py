from backend.itrabaho import models, serializers
from django.contrib.auth import authenticate
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.settings import api_settings

# Create your views here.


class LoginController(viewsets.GenericViewSet):
    serializer_class = serializers.UserModelSerializer
    queryset = models.UserModel.objects.all()

    @swagger_auto_schema(
        request_body=serializers.LoginRequestSerializer(),
        responses={
            200: serializers.UserModelSerializer(),
            400: "`string`",
        },
    )
    @action(methods=["POST"], detail=False)
    def login(self, request):
        serializer = serializers.LoginRequestSerializer(data=request.data)
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
        return Response(serializers.UserModelSerializer(user).data)

    def checkUserExist(self, phoneNumber):
        return models.UserModel.objects.filter(phoneNumber=phoneNumber)
