__author__ = 'kbushko'
from django.contrib.auth.models import User
from django.db import models

class AppStore(models.Model):
    user=models.CharField(max_length=80)
    name=models.CharField(max_length=80)
    path=models.CharField(max_length=256)
    size=models.BigIntegerField(default=0)
    description=models.CharField(max_length=1024)
    url=models.URLField(default="http://www.android.com")

    packageName=models.CharField(max_length=256)
    versionName=models.CharField(max_length=80)
    versionCode=models.IntegerField(default=0)

    five_stars=models.BigIntegerField(default=0)
    four_stars=models.BigIntegerField(default=0)
    three_stars=models.BigIntegerField(default=0)
    two_stars=models.BigIntegerField(default=0)
    one_stars=models.BigIntegerField(default=0)
    total_rating=models.BigIntegerField(default=0)

    date=models.DateTimeField(auto_now_add=True)
    downloads=models.BigIntegerField(default=0)


class RateApp(models.Model):
    user=models.ForeignKey(User)
    app=models.ForeignKey(AppStore)
    rating=models.IntegerField(default=0)
    comment=models.CharField(max_length=256)
    date=models.DateTimeField(auto_now_add=True)