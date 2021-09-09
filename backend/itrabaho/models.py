from django.db import models
from backend.globals import (
    DEFAULT_MAX_LENGTH,
    LONG_MAX_LENGTH,
    MOBILE_NUMBER_MAX_LENGTH,
)
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from backend.itrabaho.choices import SexChoices

from backend.itrabaho import managers

# Create your models here.


class User(AbstractUser, PermissionsMixin):
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    firstName = models.CharField(max_length=DEFAULT_MAX_LENGTH)
    lastName = models.CharField(max_length=DEFAULT_MAX_LENGTH)
    phoneNumber = models.CharField(max_length=MOBILE_NUMBER_MAX_LENGTH, unique=True)
    sex = models.CharField(max_length=1, choices=SexChoices.choices)
    birthDate = models.DateField(blank=True, null=True)

    objects = managers.UserManager()

    USERNAME_FIELD = "phoneNumber"

    def __str__(self):
        return f"{self.phoneNumber} - {self.lastname}, {self.firstName}"
