from django.db.models import base
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from backend.itrabaho import controllers

ROUTER = DefaultRouter()

ROUTER.register("", controllers.LoginController)
ROUTER.register("applicants", controllers.ApplicantController)
ROUTER.register("jobs", controllers.JobPostController)

urlpatterns = path("", include(ROUTER.urls))
