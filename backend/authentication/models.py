from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .manager import UserManager

class User(AbstractBaseUser, PermissionsMixin):
  
  # required fields for registration
  username = models.CharField(unique=True, max_length=25)
  email = models.EmailField(unique = True)
  password = models.CharField(max_length = 100)
  
  # optional for profile
  first_name = models.CharField(max_length = 100, null=True, blank=True)
  last_name = models.CharField(max_length = 100, null=True, blank=True)
  profile_picture = models.ImageField(upload_to = 'profile_pictures/', blank = True, null = True)
  phone_number = models.CharField(max_length = 15,unique=True, blank = True, null = True)
  address = models.CharField(max_length = 255, blank = True, null = True)
  
  # to track whether user is an organizer or not
  is_organizer = models.BooleanField(default = False)
  
  # fields for superadmin 
  is_active = models.BooleanField(default = True)
  is_staff = models.BooleanField(default = False)
  is_superuser = models.BooleanField(default = False)
  
  created_at = models.DateTimeField(auto_now_add = True)
  updated_at = models.DateTimeField(auto_now = True)
  last_login = models.DateTimeField(auto_now = True)
  
  
  USERNAME_FIELD = 'email' # field to use for login
  REQUIRED_FIELDS = [] # required fields for creating superuser
  
  objects = UserManager()
  
  def __str__(self):
    return self.username
  
  
  
  
  
  
  