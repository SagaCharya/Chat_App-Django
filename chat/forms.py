from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, UserProfile
from django import forms
from django.forms import ModelForm




class ProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ["profile_pic", "bio"]

class FileUploadForm(forms.Form):
    file = forms.FileField()
    
    