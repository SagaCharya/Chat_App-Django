from django.urls import path
from . import views


urlpatterns = [
    path('home/', views.home, name='home'),
    path('friends/', views.friends_list, name='friends'),
    path('friend_request/', views.friends_request, name='friend_request'),
    path('add_friend/<int:request_id>/', views.accept_friend_request, name='add_friend'),
    path('remove_friend/<int:user_id>/', views.remove_friend, name='remove_friend'),
    path('search_users/', views.search_users, name='search_users'),
    path('send_friend_request/<int:user_id>/', views.send_friend_request, name='send_friend_request'),
    path('chat_detail/<int:user_id>/', views.chat_detail, name='chat_detail'),
    path('profile/',views.profile, name='profile'),
    path('user_profile/',views.user_profile , name='user_profile' ),
    path('change_password/',views.change_password_btn, name='change_password'),
    path('recent_chats_partial/',views.recent_chats_partial, name='recent_chats_partial'),
    path('search_chats',views.search_chats, name='search_chats'),
]

