from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import AbstractBaseUser

from django.contrib.auth.base_user import BaseUserManager
from django.utils import timezone

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
    sheet_id = models.CharField(max_length=255, unique=True)
    date = models.DateField(auto_now_add=True, null=True)

    def email_open(self):
        opened = Campaign.objects.filter(sheet_id=self.sheet_id).first()
        return opened.tracker.count()

    def __str__(self):
        return self.sheet_id

    class Meta:
        ordering = ['-date']


class TrackingImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=255)
    action = models.CharField(max_length=255)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, null=True, related_name='tracker')
    rowIdx = models.CharField(max_length=255)

    def __str__(self):
        return self.email


class UnsubscribeEmail(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, null=True, related_name='unsubscribed')
    email = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class Plans(models.Model):
    PLAN_TYPE = (
        ('Free', 'Free'),
        ('Paid', 'Paid')
    )
    name = models.CharField(max_length=120)
    cost = models.CharField(max_length=20, help_text='Cost of Plan in USD', null=True)
    type = models.CharField(choices=PLAN_TYPE, default='Free', max_length=10)
    description = models.TextField(null=True)
    quota = models.CharField(max_length=120, help_text='Quota per 24 hrs', default=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = ('Plans')


class PurchasedPlans(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_plan')
    plan = models.ForeignKey(Plans, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.plan.name

    class Meta:
        verbose_name_plural = ('Purchased Plans')


class QuotaConsumed(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userquota_consumed')
    amount = models.IntegerField(default=0)
    date = models.DateField(default=timezone.now)
