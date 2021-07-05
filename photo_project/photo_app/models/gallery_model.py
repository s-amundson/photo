from django.conf import settings
from django.db import models
from .photo_model import PhotoModel


# Create your models here.
class Gallery(models.Model):
    can_public = models.BooleanField(default=False)
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    photo_model = models.ForeignKey(PhotoModel, on_delete=models.SET_NULL, null=True, default=None)
    public_date = models.DateField(null=True, default=None)
    shoot_date = models.DateField(null=True, default=None)
