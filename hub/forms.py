from django import forms
from .models import Project

class CreateProject(forms.ModelForm):
    img = forms.ImageField()
    class Meta:
        model = Project
        fields = '__all__'

class Login(forms.ModelForm):
    username = forms.CharField()
    password = forms.PasswordInput()

class Register(forms.ModelForm):
    username = forms.CharField()
    password = forms.PasswordInput()
    email = forms.CharField()