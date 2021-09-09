from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, phoneNumber, password, **kwargs):
        user = self.model(phoneNumber=phoneNumber, **kwargs)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, phoneNumber, password=None, **kwargs):
        user = self.create_user(phoneNumber, password, **kwargs)

        user.is_staff = True
        user.is_superuser = True

        user.save()

        return user
