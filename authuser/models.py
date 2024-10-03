# authuser/models.py
from typing import Any
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models
from django.utils import timezone
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password

class CustomUserManager(UserManager):
    def _create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')
        if not email:
            raise ValueError('You have not provided a valid e-mail address')
        
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)  # 直接設置原始密碼
        user.save(using=self._db)
        
        return user
    
    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        
        return self._create_user(username, email, password, **extra_fields)
    
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        return self._create_user(username, email, password, **extra_fields)
    
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(blank=True, default='', unique=True)
    name = models.CharField(max_length=255, blank=True, default='')
    
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)
    
        # 新增的字段
    resident_id = models.CharField(max_length=50, blank=True)
    resident_name = models.CharField(max_length=50, blank=True)
    resident_description = models.CharField(max_length=200, blank=True)
    resident_contact_person = models.CharField(max_length=80, blank=True)
    resident_contact_phone = models.CharField(max_length=100, blank=True)
    resident_contact_email = models.CharField(max_length=100, blank=True)
    resident_contact_relation = models.CharField(max_length=100, blank=True)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        
    def get_full_name(self):
        return self.name
    
    def get_short_name(self):
        return self.name or self.email.split('@')[0]

