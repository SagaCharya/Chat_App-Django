from .views import recent_chats

def chat_sidebar(request):
    if request.user.is_authenticated:
        return recent_chats(request)
    return {}
