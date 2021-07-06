from django.conf import settings
from django.db import models


def content_file_name(instance, filename):
    return '/'.join(['release', str(instance.release.id), filename])


class Release(models.Model):
    file = models.FileField(upload_to='release')
    name = models.CharField(max_length=100)
    photographer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    photo_model = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, default=None)
    shoot_date = models.DateField(null=True, default=None)
    signature = models.ImageField(upload_to='release')
