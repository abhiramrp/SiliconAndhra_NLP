from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group

class CustomUserManager(BaseUserManager):
  def create_user(self, email, first_name, last_name, password, role, **extra_fields):
    if not email:
      raise ValueError(_("The Email must be set"))
    
    email = self.normalize_email(email)
    user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
    user.set_password(password)
    user.save()
    
    group = Group.objects.get(name=role)
    user.groups.add(group)

    return user
  
  def create_superuser(self, email, first_name, last_name, password, **extra_fields):

    extra_fields.setdefault("is_staff", True)
    extra_fields.setdefault("is_superuser", True)
    extra_fields.setdefault("is_active", True)
    extra_fields.setdefault("role", 'Admin')

    if extra_fields.get("is_staff") is not True:
      raise ValueError(_("Superuser must have is_staff=True."))
    if extra_fields.get("is_superuser") is not True:
      raise ValueError(_("Superuser must have is_superuser=True."))
    
    return self.create_user(email, first_name, last_name, password, "Admin", **extra_fields)