from django.db import models

from ..models import Contact


class Link(models.Model):
    account = models.CharField(max_length=100)
    person = models.ForeignKey(Contact, on_delete=models.CASCADE)
    service = models.CharField(max_length=50)
