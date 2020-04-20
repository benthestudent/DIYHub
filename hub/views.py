from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, 'hub/DIYHUB.html')


def login(request):
    return render(request, 'hub/login.html')


def register(request):
    return render(request, 'hub/register.html')


def profile(request):
    return render(request, 'hub/profile.html')


def createProject(request):
    return render(request, 'hub/createProject.html')


def project(request):
    return render(request, 'hub/project.html')
