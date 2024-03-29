from django.db import models

from ..fields import PhoneField
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    dob = models.DateField(null=True, default=None)
    city = models.CharField(max_length=150)
    is_model = models.BooleanField(default=True)
    is_photographer = models.BooleanField(default=False)
    nickname = models.CharField(max_length=100, null=True, default=None)
    post_code = models.CharField(max_length=10)
    phone = PhoneField(max_length=20, null=True, default=None)
    state = models.CharField(max_length=3)
    street = models.CharField(max_length=150)
    use_real_name = models.BooleanField(default=True)

    def __str__(self):  # pragma: no cover
        return f'{self.first_name} {self.last_name}'
