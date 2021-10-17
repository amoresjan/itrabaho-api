from typing import Match

from django.db.models import TextChoices
from django.db.models.enums import IntegerChoices


class SexChoices(TextChoices):
    MALE = ("M", "Male")
    FEMALE = ("F", "Female")


class StatusChoices(TextChoices):
    EMPLOYED = ("E", "Employed")
    UNEMPLOYED = ("U", "Unemployed")


class AcademicLevelChoices(TextChoices):
    NONE = ("N", "None")
    ELEMENTARY = ("E", "Elementary")
    HIGH_SCHOOL = ("H", "High School")
    UNDER_GRAD = ("U", "College Undergraduate")
    BACHELORS_DEGREE = ("B", "Bachelor's Degree")
    ASSOCIATE_DEGREE = ("A", "Associate Degree")
    MASTERS_DEGREE = ("M", "Master's Degree")
    DOCTORATE = ("D", "Doctorate Degree")


class ActivityTypeChoices(TextChoices):
    MATCH = ("M", "Match")
    REVIEW = ("R", "Review")
    ACCEPTED = ("A", "Accepted")


class JobPostStatusChoices(TextChoices):
    HIRING = ("H", "Hiring")
    ACTIVE = ("A", "Active")
    DONE = ("D", "Done")


class UserTypeChoices(TextChoices):
    RECRUITER = ("R", "Recruiter")
    APPLICANT = ("A", "Applicant")
    LGUREPRESENTATIVE = ("L", "LGU Representative")
