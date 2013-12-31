__author__ = 'kbushko'
from django.db import models

class AppStore(models.Model):
    name=models.CharField(max_length=80)
    path=models.CharField(max_length=256)
    description=models.CharField(max_length=256)
    date=models.DateTimeField(auto_now_add=True)
