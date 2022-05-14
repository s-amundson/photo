from django.db import models

from .contact import Contact


class Comment(models.Model):
    comment = models.TextField()
    comment_date = models.DateTimeField(auto_now=True)
    person = models.ForeignKey(Contact, on_delete=models.CASCADE)
