from django.conf import settings
from django.db import models


class Gallery(models.Model):
    description = models.CharField(max_length=255, default='')
    display_image = models.ForeignKey('photo_app.Images', default=None, null=True, on_delete=models.SET_NULL,
                                      related_name='display')
    is_mature = models.BooleanField(default=False)
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1,
                              related_name='gallery_owner')
    public_date = models.DateField(null=True, default=None)
    photographer = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='photographers', default=None)
    privacy_choices = [('public', 'Public'), ('authenticated', 'Authenticated'), ('private', 'Private')]
    privacy_level = models.CharField(max_length=40, null=True, choices=privacy_choices, default='private')
    release = models.ManyToManyField('photo_app.Release', related_name='releases')
    shoot_date = models.DateField(null=True, default=None)
    talent = models.ManyToManyField('photo_app.Talent')
