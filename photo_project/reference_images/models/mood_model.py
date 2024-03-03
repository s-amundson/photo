from django.db import models
import uuid

from photo_app.models import Images
from .reference_model import Reference


def content_file_name(instance, filename):
    return '/'.join(['reference', filename])


def thumb_file_name(instance, filename):
    return '/'.join(['images', str(instance.gallery.id), 'thumb', filename])


# Create your models here.
class MoodImage(models.Model):
    comment = models.CharField(max_length=255)
    image = models.ForeignKey(Images, on_delete=models.CASCADE, null=True, default=None)
    reference_image = models.ForeignKey(Reference, on_delete=models.CASCADE, null=True, default=None)


class Mood(models.Model):
    mood_image = models.ManyToManyField(MoodImage)
    random_url = models.UUIDField(default=uuid.uuid4)
    is_public = models.BooleanField(default=True)
