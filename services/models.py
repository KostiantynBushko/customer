from django.db import models

# Create your models here.

class MapPoint(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    time = models.DateTimeField(auto_now_add=True)

class Track(models.Model):
    username = models.CharField(max_length=80)
    track = models.ForeignKey(MapPoint)
    start = models.DateTimeField(auto_now_add=True)
    finish = models.DateTimeField()