from django.conf import settings
from django.db import models
from django.utils import timezone


class Comment(models.Model):
    comment = models.TextField()
    comment_date = models.DateTimeField(auto_now=True)
    image = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

