__author__ = 'kbushko'
from django.db import models

class Message(models.Model):
    username=models.CharField(max_length=80)
    sender=models.CharField(max_length=80)
    message=models.CharField(max_length=256)
    date=models.DateTimeField(auto_now_add=True)

