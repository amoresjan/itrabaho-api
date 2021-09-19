from django.urls import include, path
from rest_framework.routers import DefaultRouter

from backend.itrabaho import controllers


ROUTER = DefaultRouter()

ROUTER.register("login", controllers.LoginController)

urlpatterns = path("", include(ROUTER.urls))
