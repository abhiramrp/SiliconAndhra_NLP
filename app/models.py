from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager

# Create your models here.


class CustomUser(AbstractBaseUser, PermissionsMixin):
  email = models.EmailField(_("email address"), unique=True)
  is_staff = models.BooleanField(default=False)
  is_superuser = models.BooleanField(default=False)
  is_active = models.BooleanField(default=True)
  date_joined = models.DateTimeField(default=timezone.now)

  first_name = models.CharField(max_length=35)
  last_name = models.CharField(max_length=35)

  USERNAME_FIELD = "email"
  REQUIRED_FIELDS = ['first_name', 'last_name']

  objects = CustomUserManager()

  def __str__(self):
    return self.email