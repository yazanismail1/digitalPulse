from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    pass

    def __str__(self):
        return self.username

class UserProfile(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=100, unique=True, blank=True, null=True)
    phoneNumber = models.PositiveBigIntegerField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, blank=True, null=True, related_name="userProfile")