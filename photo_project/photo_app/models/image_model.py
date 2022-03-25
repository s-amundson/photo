from django.db import models
from .gallery_model import Gallery


def content_file_name(instance, filename):
    return '/'.join(['images', str(instance.gallery.id), filename])


def thumb_file_name(instance, filename):
    return '/'.join(['images', str(instance.gallery.id), 'thumb', filename])


# Create your models here.
class Images(models.Model):
    active = models.BooleanField(default=True)
    camera_make = models.CharField(default=None, max_length=50)
    camera_model = models.CharField(default=None, max_length=50)
    gallery = models.ForeignKey(Gallery, on_delete=models.DO_NOTHING)
    filename = models.CharField(max_length=200)
    image = models.ImageField(upload_to=content_file_name)
    height = models.IntegerField()
    orientation = models.IntegerField()
    # Privacy:
    #   Photographer only is for just the photographer, used for records ect.
    #   Private is for only the photographer and talent.
    #   Public can be shared with anyone.
    privacy_choices = [('photographer', 'Photographer Only'), ('private', 'Private'), ('public', 'Public')]
    privacy_level = models.CharField(max_length=40, null=True, choices=privacy_choices, default='private')
    tags = models.CharField(max_length=255)
    taken = models.DateTimeField(default=None, blank=True, null=True)
    thumb = models.ImageField(upload_to=thumb_file_name)
    thumb_width = models.IntegerField()
    width = models.IntegerField()

    def __str__(self):
        return self.filename
