from django.db import models
from django.contrib.postgres.fields import ArrayField
from jsonfield import JSONField
from django.contrib.auth.models import User
from datetime import datetime

class PartCategories(models.Model):
    name = models.TextField()

class ProjectCategories(models.Model):
    name = models.TextField()

class Parts(models.Model):
    name = models.TextField()
    url = models.TextField(null=True)
    category = models.ForeignKey(PartCategories, default=0, on_delete=models.CASCADE)

class Project(models.Model):
    imgPath = models.TextField(null=True)
    name = models.TextField(unique=True)
    desc = models.TextField()
    difficulty = models.IntegerField(default=0)
    url = models.TextField(null=True, unique=True)
    steps = models.TextField(null=True)
    parts = models.TextField(null=True)
    partIDs = ArrayField(models.IntegerField(), null=True)
    category = models.ForeignKey(ProjectCategories, default=1, on_delete=models.CASCADE)
    #partsNeeded = ArrayField(ArrayField(models.TextField(max_length=50, null=True, blank=True), null=True), null=True)
    upvotes = models.IntegerField(default=0)
    dateCreated = models.DateTimeField(default=datetime.now, blank=True)
    author = models.ManyToManyField(User)
    views = models.IntegerField(default=0)

# class User(models.Model):
#     username = models.TextField()
#     password = models.TextField()
#     email = models.TextField()
#     #phone = models.IntegerField()
#     #profilePicture = models.TextField()
#     #bio = models.TextField()
#     #parts = ArrayField(models.TextField(), blank=True)
#     #projects = ArrayField(models.TextField(), blank=True)
#     #savedProjects = ArrayField(models.TextField(), blank=True)

class Comment(models.Model):
    body = models.TextField()
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    upvotes = models.IntegerField(default=0)
    project = models.ManyToManyField(Project, blank=True)
    commentParent = models.ManyToManyField("Comment", blank=True)

class Upvote(models.Model):
    user = models.ManyToManyField(User)
    project = models.ManyToManyField(Project, blank=True)
    comment = models.ManyToManyField(Comment, blank=True)

