from django.conf import settings
from django.db import models
from django.utils.datetime_safe import datetime


def content_file_name(instance, filename):
    return '/'.join(['release', str(instance.release.id), filename])


class ReleaseTemplate(models.Model):
    add_date = models.DateTimeField(default=datetime.now)
    file = models.FileField(upload_to='release_templates')
    name = models.CharField(max_length=100)
    update_date = models.DateTimeField(auto_now=True)
    # photographer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    # photo_model = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, default=None)
    # shoot_date = models.DateField(null=True, default=None)
    # signature = models.ImageField(upload_to='release')
