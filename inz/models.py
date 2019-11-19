from django.db import models
from django.conf import settings
# Create your models here.
from rest_framework.permissions import BasePermission

from django.contrib.auth.models import (AbstractBaseUser,BaseUserManager,PermissionsMixin)
from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, null=True)
    last_name = models.CharField(_('last name'), max_length=30, null=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Picture(models.Model):
    picture = models.ImageField()
    created_at = models.DateTimeField(auto_now_add=True)


class Receipt(models.Model):
    shop = models.CharField(max_length=50, blank=True)
    date = models.DateField(null=True)
    user = models.ForeignKey(User, models.SET_NULL,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.OneToOneField(Picture, on_delete=models.CASCADE, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __int__(self):
        return self.pk

    def getProducts(self):
        return Product.objects.filter(receipt=self)


class Product(models.Model):
    name = models.CharField(max_length=50)
    amount = models.IntegerField(default=1)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    receipt = models.ForeignKey(Receipt, models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



