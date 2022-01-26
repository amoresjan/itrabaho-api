from backend.itrabaho.serializers import base
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from backend.itrabaho import controllers

ROUTER = DefaultRouter()

ROUTER.register("", controllers.LoginController)
ROUTER.register("", controllers.SignUpController)
ROUTER.register("", controllers.ReviewController)
ROUTER.register("", controllers.ActivityFeedController)
ROUTER.register("", controllers.SkillsViewSet)
ROUTER.register("", controllers.MatchViewSet)
ROUTER.register("applicants", controllers.ApplicantController)
ROUTER.register("jobs", controllers.JobPostController)
ROUTER.register("recruiters", controllers.RecruiterController)

urlpatterns = path("", include(ROUTER.urls))
