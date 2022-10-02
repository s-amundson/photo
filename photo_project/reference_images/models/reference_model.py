from django.db import models
from photo_app.src import OverwriteStorage

from .category_model import Category


def content_file_name(instance, filename):
    return '/'.join(['reference', filename])


def thumb_file_name(instance, filename):
    return '/'.join(['images', str(instance.gallery.id), 'thumb', filename])


# Create your models here.
class Reference(models.Model):
    active = models.BooleanField(default=True)
    category = models.ManyToManyField(Category)
    image = models.ImageField(upload_to=content_file_name)
    is_model_mayhem = models.BooleanField(default=False)
    link = models.URLField(null=True, default=None)
    note = models.CharField(max_length=255)
