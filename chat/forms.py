from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django import forms


class RegisterForm(UserCreationForm):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(forms.Form):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    
    