from django.contrib import admin
from .models import CustomUser, UserProfile, FriendRequest, Message

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(UserProfile)
admin.site.register(FriendRequest)
admin.site.register(Message)
