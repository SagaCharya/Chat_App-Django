from django.shortcuts import get_object_or_404, render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import FriendRequest, CustomUser, Message
from django.db.models import Q


def index(request):
    return render(request, 'index.html')


def home(request):
    return render(request, 'home.html')

def message_list(request):
    users = CustomUser.objects.get(username=request.user)
    return render(request, 'nav/left_nav.html', {'users': users})

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
    return render(request, 'friend.html', {'friends': frineds})

@login_required
def friends_request(request):
    pending_requests = FriendRequest.objects.filter(to_user=request.user, accepted=False)
    return render(request, 'friend_req.html', {'pending_requests': pending_requests})

@login_required
def search_users(request):
    query = request.GET.get('q')
    if query:
        users = CustomUser.objects.filter(username__icontains=query).exclude(id=request.user.id)
        return render(request, 'search_user.html', {'users': users}) 
    else:
        return render(request, 'search_user.html')

@login_required
def send_friend_request(request, user_id):
    to_user = CustomUser.objects.get(id=user_id)
    FriendRequest.objects.create(from_user=request.user, to_user=to_user)
    return redirect('friends')

def accept_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id, to_user=request.user, accepted=False)
    request.user.accept_friend_request(friend_request.from_user)
    return redirect('friend_request')

def remove_friend(request, user_id):
    friend = get_object_or_404(CustomUser, id=user_id)
    request.user.remove_friend(friend)
    return redirect('friends')
    


@login_required
def recent_chats(request):
    # Get all messages sent or received by the user, ordered by timestamp
    recent_messages = Message.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user)
    ).order_by('-timestamp')  # Fetch all recent messages ordered by timestamp

    # Create a dictionary to store the last message per user
    last_messages = {}
    message_times = {}

    for msg in recent_messages:
        other_user = msg.receiver if msg.sender == request.user else msg.sender
        
        # If we haven't seen a message from this user yet, or the current message is more recent, update
        if other_user not in last_messages:
            last_messages[other_user] = msg
            message_times[other_user] = msg.timestamp

    # Get the list of users (chat_users) who had recent chats
    chat_users = list(last_messages.keys())

    # Return the data to the template context
    return {
        'chat_users': chat_users, 
        'last_messages': last_messages, 
        'message_times': message_times
    }