from django.conf import settings
from django.db import models


class Gallery(models.Model):
    is_mature = models.BooleanField(default=False)
    is_public = models.BooleanField(default=False)
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1,
                              related_name='gallery_owner')
    # photo_model = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
    # blank=True, null=True, default=None)
    photo_model = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='models')
    public_date = models.DateField(null=True, default=None)
    photographer = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='photographers')
    shoot_date = models.DateField(null=True, default=None)
