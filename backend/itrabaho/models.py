from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from twilio.rest import Client

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
    JobPostStatusChoices,
    SexChoices,
    StatusChoices,
    UserTypeChoices,
)


class UserModel(AbstractBaseUser, PermissionsMixin):
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    firstName = models.CharField(max_length=DEFAULT_MAX_LENGTH)
    lastName = models.CharField(max_length=DEFAULT_MAX_LENGTH)
    phoneNumber = models.CharField(max_length=MOBILE_NUMBER_MAX_LENGTH, unique=True)
    sex = models.CharField(max_length=1, choices=SexChoices.choices)
    birthDate = models.DateField(blank=True, null=True)
    lastLogin = models.DateField(null=True, blank=True)

    userType = models.CharField(
        max_length=1, choices=UserTypeChoices.choices, null=True, blank=True
    )

    objects = managers.UserManager()

    USERNAME_FIELD = "phoneNumber"

    def getFullName(self):
        return f"{self.firstName} {self.lastName}"

    def __str__(self):
        return f"{self.id} - {self.userType} - {self.lastName}, {self.firstName}"

    class Meta:
        verbose_name = "User"


class LGURepresentativeModel(UserModel):
    barangay = models.CharField(max_length=DEFAULT_MAX_LENGTH)
    city = models.CharField(max_length=DEFAULT_MAX_LENGTH)
    province = models.CharField(max_length=DEFAULT_MAX_LENGTH)

    def save(self, *args, **kwargs):
        self.userType = "L"
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "LGU Representative"


class RecruiterModel(UserModel):
    address = models.CharField(max_length=LONG_MAX_LENGTH)

    def save(self, *args, **kwargs):
        self.userType = "R"
        super().save(*args, **kwargs)

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
    company = models.CharField(max_length=DEFAULT_MAX_LENGTH, null=True, blank=True)
    location = models.CharField(max_length=LONG_MAX_LENGTH)
    startMonth = models.CharField(max_length=SMALL_MAX_LENGTH)
    startYear = models.CharField(max_length=SMALL_MAX_LENGTH)
    endMonth = models.CharField(max_length=SMALL_MAX_LENGTH)
    endYear = models.CharField(max_length=SMALL_MAX_LENGTH)

    # Foreign Keys
    profile = models.ForeignKey(
        ProfileModel, on_delete=models.CASCADE, related_name="experiences"
    )

    class Meta:
        verbose_name = "Experience"


class ExperienceDetailModel(models.Model):
    description = models.CharField(max_length=LONG_MAX_LENGTH)

    # Foreign Keys
    experience = models.ForeignKey(
        ExperienceModel, on_delete=models.CASCADE, related_name="details"
    )

    class Meta:
        verbose_name = "Experience Detail"


class SkillModel(models.Model):
    name = models.CharField(max_length=DEFAULT_MAX_LENGTH)

    class Meta:
        verbose_name = "Skill"


class ApplicantModel(UserModel):
    address = models.CharField(max_length=LONG_MAX_LENGTH)
    status = models.CharField(max_length=1, choices=StatusChoices.choices)

    # Foreign Keys
    profile = models.OneToOneField(ProfileModel, on_delete=models.CASCADE)
    LGURepresentativeId = models.ForeignKey(
        LGURepresentativeModel, on_delete=models.CASCADE
    )
    skills = models.ManyToManyField(SkillModel)

    def save(self, *args, **kwargs):
        self.userType = "A"
        super().save(*args, **kwargs)

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

    def __str__(self) -> str:
        return f"{self.id} / toID: {self.toUserId_id} / fromID: {self.fromUserId_id}"

    class Meta:
        verbose_name = "Review"


class JobPostModel(models.Model):
    street = models.CharField(max_length=DEFAULT_MAX_LENGTH)
    barangay = models.CharField(max_length=DEFAULT_MAX_LENGTH)
    city = models.CharField(max_length=DEFAULT_MAX_LENGTH)
    province = models.CharField(max_length=DEFAULT_MAX_LENGTH)
    status = models.CharField(
        max_length=1,
        choices=JobPostStatusChoices.choices,
        null=True,
        blank=True,
        default=JobPostStatusChoices.HIRING,
    )
    description = models.TextField()
    role = models.CharField(max_length=DEFAULT_MAX_LENGTH)
    datetimeCreated = models.DateTimeField(auto_now_add=True)
    datetimeEnded = models.DateTimeField(null=True, blank=True)
    title = models.CharField(max_length=LONG_MAX_LENGTH)
    skills = models.ManyToManyField(SkillModel)

    # Foreign Keys
    applicantId = models.ForeignKey(
        ApplicantModel,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="accepted_jobs",
    )
    recruiterId = models.ForeignKey(
        RecruiterModel, on_delete=models.CASCADE, related_name="posted_jobs"
    )
    applicantReviewId = models.OneToOneField(
        ReviewModel, on_delete=models.CASCADE, null=True, blank=True, related_name="job"
    )
    recruiterReviewId = models.OneToOneField(
        ReviewModel,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="my_job_post",
    )

    def __str__(self) -> str:
        return f"{self.id} / {self.title} / recruiterId: {self.recruiterId_id} / { self.status }"

    class Meta:
        verbose_name = "Job Model"


class ApplicantsListModel(models.Model):
    # Foreign Keys
    jobPostId = models.ForeignKey(JobPostModel, on_delete=models.CASCADE)
    applicantId = models.ForeignKey(ApplicantModel, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "ApplicantsList"
        default_related_name = "job_applications"


class ActivityModel(models.Model):
    type = models.CharField(max_length=1, choices=ActivityTypeChoices.choices)
    datetimeCreated = models.DateTimeField(auto_now_add=True)
    objectId = models.PositiveSmallIntegerField()

    # Foreign Keys
    contentType = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    contentObject = GenericForeignKey("contentType", "objectId")

    def __str__(self):
        return f"{self.type} / {self.id} - {self.contentObject}"

    class Meta:
        verbose_name = "Activity"
        verbose_name_plural = "Activities"


class MatchModel(models.Model):
    rank = models.PositiveSmallIntegerField()
    percentage = models.PositiveSmallIntegerField()

    # Foreign Keys
    jobPostId = models.ForeignKey(JobPostModel, on_delete=models.CASCADE)
    applicantId = models.ForeignKey(ApplicantModel, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Match"
        verbose_name_plural = "Matches"
