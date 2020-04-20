from django.db import models

class Project(models.Model):
    name = models.TextField()
    desc = models.TextField()

class User(models.Model):
    username = models.TextField()
    password = models.TextField()
    email = models.TextField()
    phone = models.IntegerField