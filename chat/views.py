from datetime import timedelta
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from .forms import ProfileForm
from django.contrib.auth.decorators import login_required
from .models import FriendRequest,  Message
from django.db.models import Q, OuterRef, Subquery
from user.models import CustomUser
from user.tasks import send_password_change_email
import uuid
from django.core.exceptions import ObjectDoesNotExist
from .utils.decorators import active_profile_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt



@login_required
def change_password_btn(request):
    try:
        user = request.user
        # Generate a unique verification token
        user.verification_token = uuid.uuid4().hex
        user.token_created_at = timezone.now()
        user.save()

        # Create the verification link
        verification_link = f"http://127.0.0.1:8000/password_change/{user.verification_token}/"
        
        send_password_change_email.delay(user.email, verification_link)
        messages.success(request, 'Verification for the password Change has been sent to your email')
        # Render the success page
        return redirect('user_profile')

    except Exception as e:
        print(e)
        return redirect('user_profile')
    

@active_profile_required
@login_required
def home(request):
        return render(request, 'home.html')



@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST,request.FILES, instance=request.user.profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.is_active = True
            profile.save()
            return redirect('home')
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'profile.html', {'form':form})

@login_required
def user_profile(request):
    user = CustomUser.objects.get(id = request.user.id)
    return render(request, 'user_profile.html', {'user':user})




@login_required
@active_profile_required
def friends_list(request):
        frineds = request.user.friends.all()
        return render(request, 'friend.html', {'friends': frineds})

@login_required
@active_profile_required
def friends_request(request):
        pending_requests = FriendRequest.objects.filter(to_user=request.user, accepted=False)
        return render(request, 'friend_req.html', {'pending_requests': pending_requests})

@login_required
def search_users(request):
        query = request.GET.get('q')
        user = request.user
        if query:
            friends = user.friends.all()
            users = CustomUser.objects.filter(username__icontains=query).exclude(id=request.user.id).exclude(friends__in=friends)
            return render(request, 'search_user.html', {'users': users}) 
        else:
            user = CustomUser.objects.none()
        
@login_required
@active_profile_required
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

    last_messages_subquery = Message.objects.filter(
        Q(sender=OuterRef('sender'),receiver=OuterRef('receiver'))|
        Q(sender=OuterRef('receiver'), receiver=OuterRef('sender'))
        ).order_by('-timestamp').values('id')[:1]   
    
   

    recent_messages = Message.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user)
    ).filter(
        id__in=Subquery(last_messages_subquery)  
    ).order_by('-timestamp')
    
    last_messages = {}
    message_times = {}

    print(f"Recent Messages: {recent_messages}")
    
    for msg in recent_messages:
        other_user = msg.receiver if msg.sender == request.user else msg.sender
        

        # If we haven't seen a message from this user yet, or the current message is more recent, update
        if other_user not in last_messages:
            if msg.file and not msg.content.strip():
                 if msg.file.url.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg')):
                    last_messages[other_user] = "📷 Image"
                 else:
                    last_messages[other_user] = "📎 File "
            else:
                last_messages[other_user] = msg.content
            message_times[other_user] = msg.timestamp

          
    chat_users = list(last_messages.keys())

   
    return(
        {
        'chat_users': chat_users,
        'last_messages': last_messages,
        'message_times': message_times}
        )

@login_required
@active_profile_required
def chat_detail(request, user_id):
 
    chat_user = get_object_or_404(CustomUser, id=user_id)
    messages = Message.objects.filter(
            (Q(sender=request.user, receiver=chat_user) | Q(sender=chat_user, receiver=request.user))
        ).order_by("timestamp")

    context = {
        "chat_user": chat_user,
        "msg": messages,
    }
    
    if request.headers.get("HX-Request"):
        return render(request, "chat_window.html", context)
    else:
        context.update(recent_chats(request))
        return render(request, "home.html", context)

@login_required
def recent_chats_partial(request):
    context = recent_chats(request)  # Get updated chat data
    return render(request, "nav/left_nav.html", context)



@login_required
def search_chats(request):
    query = request.GET.get('q', '').strip()

    chat_users = CustomUser.objects.filter(
        Q(sent_messages__receiver=request.user) | 
        Q(received_messages__sender=request.user)
    ).distinct()

    # Filter based on search query
    if query:
        chat_users = chat_users.filter(username__icontains=query)

    return render(request, 'nav/chat_list.html', {'chat_users': chat_users})


@login_required
def upload_file(request):
    if request.method == 'POST':
        if not request.FILES.get('file'):
            return JsonResponse({"error": "No file uploaded"}, status=400)

        file = request.FILES["file"]
        receiver_id = request.POST.get("receiver_id")

        # Fetch receiver instance properly
        receiver = get_object_or_404(CustomUser, id=receiver_id)

        message_instance = Message.objects.create(
            sender=request.user,
            receiver=receiver, 
            content='',
            file=file
        )

        return render(request, 'part/file_preview.html', {
            'file_url': message_instance.file.url,
            'file_name': file.name
        })

    return JsonResponse({"error": "Invalid request"}, status=400)