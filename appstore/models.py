__author__ = 'kbushko'
from django.db import models

class AppStore(models.Model):
    user=models.CharField(max_length=80)
    name=models.CharField(max_length=80)
    path=models.CharField(max_length=256)
    description=models.CharField(max_length=256)
    ur=models.URLField(default="http://www.android.com")
    five_stars=models.BigIntegerField(default=0)
    four_stars=models.BigIntegerField(default=0)
    three_stars=models.BigIntegerField(default=0)
    two_stars=models.BigIntegerField(default=0)
    one_stars=models.BigIntegerField(default=0)
    date=models.DateTimeField(auto_now_add=True)
