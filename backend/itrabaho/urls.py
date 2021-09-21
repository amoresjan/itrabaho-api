from django.db.models import base
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from backend.itrabaho import controllers


ROUTER = DefaultRouter()

ROUTER.register("", controllers.LoginController, basename="login")
ROUTER.register("", controllers.ApplicantsController, basename="applicants")

urlpatterns = path("", include(ROUTER.urls))
