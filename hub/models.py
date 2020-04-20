from django.db import models
from django.contrib.postgres.fields import ArrayField

class Project(models.Model):
    name = models.TextField()
    desc = models.TextField()
    #partsNeeded = ArrayField(models.TextField(), blank=True)
    difficulty = models.IntegerField(default=0)
    #url = models.TextField()

class User(models.Model):
    username = models.TextField()
    password = models.TextField()
    email = models.TextField()
    #phone = models.IntegerField()
    #profilePicture = models.TextField()
    #bio = models.TextField()
    #parts = ArrayField(models.TextField(), blank=True)
    #projects = ArrayField(models.TextField(), blank=True)
    #savedProjects = ArrayField(models.TextField(), blank=True)

class Parts(models.Model):
    name = models.TextField()
    url = models.TextField()
