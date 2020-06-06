from django import forms
from .models import Project, Comment, User
from django.core.exceptions import ValidationError

class Register(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
    email = forms.EmailField()

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise ValidationError("Email already exists")
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        return password

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['email'],
            self.cleaned_data['username'],
            self.cleaned_data['password']
        )
        return user