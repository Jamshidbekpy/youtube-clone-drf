from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from apps.base.models import BaseModel

# Create your models here.

class MyUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email kiritish majburiy")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser `is_staff=True` ")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser `is_superuser=True`")

        return self.create_user(username, email, password, **extra_fields)





class MyUser(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(upload_to='profile_picture/', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']


    class Meta:
        ordering = ['username']
        verbose_name = 'MyUser'
        verbose_name_plural = 'MyUsers'
    def __str__(self):
        return self.username
    

from apps.base.models import BaseModel

class Channel(BaseModel):
    name = models.CharField(max_length=150)
    owner = models.OneToOneField(MyUser, on_delete=models.CASCADE,null=True, blank=True,related_name='channel')
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='channel_images/', null=True, blank=True)
    banner = models.ImageField(upload_to='channel_banners/', null=True, blank=True)
    subscribers = models.ManyToManyField(MyUser, related_name="channels", blank=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Channel'
        verbose_name_plural = 'Channels'
        
    def __str__(self):
        return self.name
    
        

class UserProfile(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    smtp_host = models.CharField(max_length=255, blank=True, null=True)
    smtp_port = models.IntegerField(default=587)
    smtp_email = models.EmailField(blank=True, null=True)
    smtp_password = models.CharField(max_length=255, blank=True, null=True)
