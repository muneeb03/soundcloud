from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

# Create your models here.

class MyUserManager(BaseUserManager):
    def create_user(self, email,full_name, password=None, password2=None):
        if not email:
            raise ValueError("User must have an email address")
        
        user = self.model(
            email=self.normalize_email(email),
            full_name = full_name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email, password, **kwargs):
        user = self.model(
            email = email, is_staff=True, is_superuser=True, is_active=True, **kwargs
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    

class User(AbstractUser):
    email=models.EmailField(max_length=254, unique=True)
    full_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notifications = models.JSONField(default=list, blank=True)
    username=None

    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]