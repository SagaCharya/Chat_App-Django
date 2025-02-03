from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('home/', views.home, name='home'),
    path('logout/', views.user_logout, name='logout'),
    path('friends/', views.friends_list, name='friends'),
    path('friend_request/', views.friends_request, name='friend_request'),
    path('add_friend/<int:request_id>/', views.accept_friend_request, name='add_friend'),
    path('remove_friend/<int:user_id>/', views.remove_friend, name='remove_friend'),
    path('search_users/', views.search_users, name='search_users'),
    path('send_friend_request/<int:user_id>/', views.send_friend_request, name='send_friend_request'),
    path('chat_detail/<int:user_id>/', views.chat_detail, name='chat_detail'),
    path('profile/',views.profile, name='profile'),
    path('user_profile/',views.user_profile , name='user_profile' ),
]

