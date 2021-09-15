from backend.globals import (
    DEFAULT_MAX_LENGTH,
    LONG_MAX_LENGTH,
    MOBILE_NUMBER_MAX_LENGTH,
    SMALL_MAX_LENGTH,
)
from backend.itrabaho import choices, managers
from backend.itrabaho.choices import (
    AcademicLevelChoices,
    ActivityTypeChoices,
    SexChoices,
    StatusChoices,
)
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.base import Model


class UserModel(AbstractBaseUser, PermissionsMixin):
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
        return f"{self.phoneNumber} - {self.lastName}, {self.firstName}"

    class Meta:
        verbose_name = "User"


class LGURepresentativeModel(UserModel):
    barangay = models.CharField(max_length=DEFAULT_MAX_LENGTH)
    city = models.CharField(max_length=DEFAULT_MAX_LENGTH)
    province = models.CharField(max_length=DEFAULT_MAX_LENGTH)

    class Meta:
        verbose_name = "LGU Representative"


class RecruiterModel(UserModel):
    address = models.CharField(max_length=LONG_MAX_LENGTH)

    class Meta:
        verbose_name = "Recruiter"


class ProfileModel(models.Model):
    yearsOfExperience = models.PositiveSmallIntegerField()
    highesteducationAttained = models.CharField(
        max_length=1, choices=AcademicLevelChoices.choices
    )

    class Meta:
        verbose_name = "Profile"


class ExperienceModel(models.Model):
    role = models.CharField(max_length=DEFAULT_MAX_LENGTH)
    company = models.CharField(max_length=DEFAULT_MAX_LENGTH)
    location = models.CharField(max_length=LONG_MAX_LENGTH)
    startMonth = models.CharField(max_length=SMALL_MAX_LENGTH)
    startYear = models.CharField(max_length=SMALL_MAX_LENGTH)
    endMonth = models.CharField(max_length=SMALL_MAX_LENGTH)
    endYear = models.CharField(max_length=SMALL_MAX_LENGTH)

    # Foreign Keys
    profile = models.ForeignKey(ProfileModel, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Experience"


class ExperienceDetailModel(models.Model):
    description = models.CharField(max_length=LONG_MAX_LENGTH)

    # Foreign Keys
    experience = models.ForeignKey(ExperienceModel, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Experience Detail"


class ApplicantModel(UserModel):
    address = models.CharField(max_length=LONG_MAX_LENGTH)
    status = models.CharField(max_length=1, choices=StatusChoices.choices)

    # Foreign Keys
    LGURepresentativeId = models.ForeignKey(
        LGURepresentativeModel, on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "Applicant"


class ReviewModel(models.Model):
    rate = models.PositiveSmallIntegerField()
    comment = models.CharField(max_length=LONG_MAX_LENGTH, null=True, blank=True)

    # Foreign Keys
    fromUserId = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name="+"
    )
    toUserId = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="+")

    class Meta:
        verbose_name = "Review"


class ActivityModel(models.Model):
    type = models.CharField(max_length=1, choices=ActivityTypeChoices.choices)
    datetime_created = models.DateTimeField(auto_now_add=True)
    label = models.CharField(max_length=LONG_MAX_LENGTH)
    contentType = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    objectId = models.PositiveSmallIntegerField()
    contentObject = GenericForeignKey("contentType", "objectId")

    # Foreign Keys
    applicant = models.ForeignKey(ApplicantModel, on_delete=models.CASCADE)
    recruiter = models.ForeignKey(RecruiterModel, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Activity"
