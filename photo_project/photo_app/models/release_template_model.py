from django.conf import settings
from django.db import models
from django.utils.datetime_safe import datetime


class ReleaseTemplate(models.Model):
    description = models.CharField(max_length=100)
    file = models.CharField(max_length=100)
