from django.db import models
from django.contrib.auth.models import (User , AbstractUser)
from django.conf import settings
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to=settings.MEDIA_ROOT+'/avatars',default='default.png',)
    is_active = models.BooleanField(default=True)


class Receipt(models.Model):
    shop = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    date = models.DateTimeField(blank=True)
    picture = models.ImageField(upload_to="",blank=True)
    user = models.ForeignKey(Profile, models.SET_NULL,null=True)


class Product(models.Model):
    name = models.CharField(max_length=50)
    amount = models.IntegerField(default=1)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    receipt = models.ForeignKey(Receipt, models.SET_NULL, null=True)


