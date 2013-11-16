from django.db import models

# Create your models here.

class Item(models.Model):
    label = models.CharField(max_length=64)
    describe = models.CharField(max_length=256)

class Menu(models.Model):
    label = models.CharField(max_length=64)


class Restaurant(models.Model):
    ovner = models.CharField(max_length=64)
    label = models.CharField(max_length=64)
    country = models.CharField(max_length=64)
    sity = models.CharField(max_length=64)
    street = models.CharField(max_length=64)
    number = models.IntegerField(null=False)
    email = models.EmailField()

