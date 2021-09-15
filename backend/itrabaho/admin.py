from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from backend.itrabaho import models

# Register your models here.

admin.site.register(models.UserModel)
admin.site.register(models.LGURepresentativeModel)
admin.site.register(models.RecruiterModel)
admin.site.register(models.ProfileModel)
admin.site.register(models.ExperienceModel)
admin.site.register(models.ExperienceDetailModel)
admin.site.register(models.ApplicantModel)