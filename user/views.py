from datetime import timedelta
from django.utils import timezone
from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser
from django.core.mail import send_mail
from django.conf import settings
import uuid
from django.utils import timezone
from .tasks import send_verification_email
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm


# Create your views here.
def index(request):
    
    return render(request, 'index.html')


# def user_register(request):
#     if request.method == 'POST':
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('login')
#     else:
#         form = RegisterForm()
#     return render(request, 'register.html', {'form': form})
def user_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user =  form.save(commit = False)
            user.is_verified = False
            user.verification_token = uuid.uuid4().hex
            user.token_created_at = timezone.now()
            user.save()

            verification_link = f"http://127.0.0.1:8000/verify/{user.verification_token}/"

            send_verification_email.delay(user.email, verification_link)
            return render(request, 'verify_email.html')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def verify_email(request, token):
    try:
        user = CustomUser.objects.get(verification_token=token)
        # Check if the token is expired (e.g., 24 hours)
        if user.token_created_at and timezone.now() - user.token_created_at <= timedelta(hours=24):
            user.is_verified = True
            user.verification_token = None
            user.save()
            return redirect('login')
        else:
            # token expires  
            return render(request,'verifiy.html')
    except CustomUser.DoesNotExist:
        return redirect('index')
    
def verify_token(request, token):
    try:
        user = CustomUser.objects.get(verification_token=token)
        # Check if the token is expired (e.g., 24 hours)
        if user.token_created_at and timezone.now() - user.token_created_at <= timedelta(hours=24):
            if request.method == 'POST':
                form = PasswordChangeForm(user, request.POST)
                if form.is_valid():
                    form.save()
                    user.verification_token = None  # Clear the token
                    user.save()
                    return redirect('login')
            else:
                form = PasswordChangeForm(user)
            
            return render(request, 'change_password.html',{'form':form})
        
            # token expires  
        return render(request,'verifiy.html')
    except CustomUser.DoesNotExist:
        return redirect('index')
    

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_verified is not False:
                    login(request, user)
                    return redirect('home')
                else:
                    return render(request, 'verify_email.html')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('index')