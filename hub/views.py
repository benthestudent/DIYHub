from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django import forms
from .models import Project
import base64
import os.path

def index(request):
    return render(request, 'hub/DIYHUB.html')


def login(request):
    return render(request, 'hub/login.html')


def register(request):
    return render(request, 'hub/register.html')


def profile(request):
    return render(request, 'hub/profile.html')


def createProject(request):
    if request.method == 'POST':
        url = request.POST.get("name").replace(" ", "-")
        imgData = request.POST.get('img').replace("data:image/jpeg;base64,", "")
        imgURL = url + ".png"
        print(imgURL)
        # with open(imgURL, "wb") as f:
        #     f.write(base64.b64decode(imgData))
        form = Project()
        form.name = request.POST.get("name")
        form.desc = request.POST.get("desc")
        form.difficulty = request.POST.get("difficulty")
        form.url = url
        form.steps = str(request.POST.get("steps"))
        forms.parts = str(request.POST.get("parts"))
        forms.imgPath = str(imgURL)
        form.save()
    return render(request, 'hub/createProject.html')


def project(request):
    return render(request, 'hub/project.html')
