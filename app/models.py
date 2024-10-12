import os
from supabase import create_client
from dotenv import load_dotenv

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager

# Create your models here.

load_dotenv()

SUPABASE_URL=os.getenv('SUPABASE_URL')
SUPABASE_KEY=os.getenv('SUPABASE_KEY')
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

class User(AbstractBaseUser, PermissionsMixin):
  email = models.EmailField(_("email address"), unique=True, primary_key=True)
  first_name = models.CharField(max_length=50)
  last_name = models.CharField(max_length=50)

  is_active = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=False)
  is_superuser = models.BooleanField(default=False)

  date_joined = models.DateTimeField(default=timezone.now)

  ROLE_CHOICES = [
    ('Admin', 'Admin'),
    ('Editor', 'Editor'), 
    ('Processing Expert', 'Processing Expert'),
    ('Annotator', 'Annotator'), 
    ('Participant', 'Participant')
  ]

  role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Participant')

  USERNAME_FIELD = "email"
  REQUIRED_FIELDS = ['first_name', 'last_name']

  objects = CustomUserManager()

  def __str__(self):
    return self.first_name + " " + self.last_name
  
SUPABASE_URL = os.getenv('SUPABASE_URL')  # Store URL in .env
SUPABASE_KEY = os.getenv('SUPABASE_KEY')  # Store API key in .env
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
  
class Document(models.Model):
  title = models.CharField(max_length=50)
  file = models.FileField(upload_to='documents/')
  uploader = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return self.title
  
  def save(self, *args, **kwargs):
    super().save(*args, **kwargs)

    with open(self.file.path, 'rb') as f:
      supabase.storage.from_("documents").upload(file=f, path="documents/")

    os.remove(self.file.path)


'''
python3 manage.py migrate
'''