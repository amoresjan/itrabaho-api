from django.db.models import TextChoices


class SexChoices(TextChoices):
    MALE = ("M", "Male")
    FEMALE = ("F", "Female")