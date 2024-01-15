from django.conf import settings
from django.db import models


class TalentCategory(models.Model):
    description = models.CharField(max_length=100)

    def __str__(self):  # pragma: no cover
        return self.description


class Talent(models.Model):
    talent = models.ForeignKey(TalentCategory, default=None, null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)

    def __str__(self):  # pragma: no cover
        return f'{self.talent} {self.user}'
