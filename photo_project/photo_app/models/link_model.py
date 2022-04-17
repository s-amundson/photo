from django.conf import settings
from django.db import models


class LinkCategory(models.Model):
    category = models.CharField(max_length=50)


class Links(models.Model):
    category = models.ForeignKey(LinkCategory, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    url = models.URLField()
