from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import AbstractBaseUser

from django.contrib.auth.base_user import BaseUserManager

# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("User must have an email address")
        user = self.model(
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.CharField(max_length=255, unique=True, verbose_name='Email Address')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class Campaign(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    campaign_uid = models.CharField(max_length=255)

    def __str__(self):
        return self.campaign_uid


class TrackingImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=255)
    uuid = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    action = models.CharField(max_length=255)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    rowIdx = models.CharField(max_length=255)

    def __str__(self):
        return self.email


class UnsubscribeEmail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    email = models.CharField(max_length=255)
    date_recorded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
