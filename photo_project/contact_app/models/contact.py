from django.db import models
from django.conf import settings

from photo_app.fields import PhoneField


class Contact(models.Model):
    email = models.EmailField(null=True, default=None, unique=True)
    first_name = models.CharField(max_length=100, null=True, default=None)
    is_model = models.BooleanField(default=True)
    last_name = models.CharField(max_length=100, null=True, default=None)
    phone = PhoneField(max_length=20, null=True, default=None)
    score = models.IntegerField(default=3) # 0 is bad 5 is great
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, default=None)


    def __str__(self):  # pragma: no cover
        return f'{self.first_name} {self.last_name}'
