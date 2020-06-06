from django.db import models
from django.contrib.postgres.fields import ArrayField
from jsonfield import JSONField
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from datetime import datetime

class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have an username")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user



class User(AbstractBaseUser):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    phone = models.BigIntegerField(null=True)
    profilePicturePath = models.TextField(null=True)
    bio = models.TextField(null=True)
    firstn = models.CharField(max_length=20, null=True)
    lastn = models.CharField(max_length=20, null=True)
    # parts = ArrayField(models.TextField(), blank=True)
    # projects = ArrayField(models.TextField(), blank=True)
    savedProjects = ArrayField(models.IntegerField(null=True), null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def is_valid(self):
        return True #make more complex



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
    # partsNeeded = ArrayField(ArrayField(models.TextField(max_length=50, null=True, blank=True), null=True), null=True)
    upvotes = models.IntegerField(default=0)
    dateCreated = models.DateTimeField(default=datetime.now, blank=True)
    author = models.ManyToManyField(User)
    views = models.IntegerField(default=0)





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
