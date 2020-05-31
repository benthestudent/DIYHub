from django.db import models
from django.contrib.postgres.fields import ArrayField
from jsonfield import JSONField

class Project(models.Model):
    imgPath = models.TextField(blank=True)
    name = models.TextField()
    desc = models.TextField()
    difficulty = models.IntegerField(default=0)
    url = models.TextField(blank=True, null=True)
    steps = models.TextField(null=True, blank=True)
    parts = models.TextField(null=True, blank=True)
    #partsNeeded = ArrayField(ArrayField(models.TextField(max_length=50, null=True, blank=True), null=True), null=True)

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
