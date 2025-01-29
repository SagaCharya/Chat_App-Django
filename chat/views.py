from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import FriendRequest, CustomUser

# Create your views here.
def index(request):
    return render(request, 'index.html')

def home(request):
    return render(request, 'home.html')

def user_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('index')


@login_required
def friends_list(request):
    frineds = request.user.friends.all()
    pending_requests = FriendRequest.objects.filter(to_user=request.user, accepted=False)
    return render(request, 'friend_list.html', {'friends': frineds, 'pending_requests': pending_requests})

@login_required
def search_users(request):
    query = request.GET.get('q')
    user = CustomUser.objects.filter(username__icontains=query)
    return render(request, 'search_users.html', {'users': user}) 

@login_required
def send_friend_request(request, user_id):
    to_user = CustomUser.objects.get(id=user_id)
    FriendRequest.objects.create(from_user=request.user, to_user=to_user)
    return redirect('search_users')

def accept_friend_request(request, request_id):
    friend_request = FriendRequest.objects.get(id=request_id)
    if friend_request.to_user == request.user:
        friend_request.accepted = True
        friend_request.save()
        request.user.friends.add(friend_request.from_user)
        friend_request.from_user.friends.add(request.user)
    return redirect('friend_list')
    