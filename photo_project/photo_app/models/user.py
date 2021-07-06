from django.conf import settings
from django.db import models

from ..fields import PhoneField
from django.contrib.auth.models import AbstractUser
from django.db.models import BooleanField, CharField, DateField


class User(AbstractUser):
    dob = models.DateField()
    city = models.CharField(max_length=150)
    is_model = models.BooleanField(default=True)
    is_photographer = models.BooleanField(default=False)
    nickname = models.CharField(max_length=50)
    post_code = models.CharField(max_length=10)
    phone = PhoneField(max_length=20)
    state = models.CharField(max_length=3)
    street = models.CharField(max_length=150)

