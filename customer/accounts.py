__author__ = 'kbushko'
from django.contrib.auth.models import User, UserManager
from django.db import models

class Customer(User):
    url = models.URLField()

    object = UserManager()
