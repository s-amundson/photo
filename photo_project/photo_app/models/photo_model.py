from django.conf import settings
from django.db import models

from ..fields import PhoneField


# Create your models here.
class PhotoModel(models.Model):
    dob = models.DateField()
    city = models.CharField(max_length=150)
    post_code = models.CharField(max_length=10)
    phone = PhoneField(max_length=20)
    state = models.CharField(max_length=3)
    street = models.CharField(max_length=150)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
