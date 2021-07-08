from django.conf import settings
from django.db import models
from .release_template_model import ReleaseTemplate


def content_file_name(instance, filename):
    return '/'.join(['release', str(instance.release.id), filename])


class Release(models.Model):
    state_list = ['pending', 'singing', 'complete', 'canceled']
    states = []
    for s in state_list:
        states.append((s, s))

    file = models.FileField(upload_to=content_file_name)
    name = models.CharField(max_length=100)
    model_signature = models.ImageField(upload_to=content_file_name)
    photographer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1,
                                     related_name='release_photographer')
    photographer_signature = models.ImageField(upload_to=content_file_name)
    photo_model = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, default=None,
                                    related_name='release_model')
    shoot_date = models.DateField(null=True, default=None)
    state = models.CharField(max_length=20, null=True, choices=states)
    template = models.ForeignKey(ReleaseTemplate, on_delete=models.DO_NOTHING)
    update_date = models.DateTimeField(auto_now=True)


