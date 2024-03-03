from django.db import models


class ReleaseTemplate(models.Model):
    description = models.CharField(max_length=100)
    file = models.CharField(max_length=100)
