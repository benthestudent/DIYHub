from django import forms
from .models import Project
class CreateProject(forms.ModelForm):
    img = forms.ImageField()
    class Meta:
        model = Project
        fields = '__all__'