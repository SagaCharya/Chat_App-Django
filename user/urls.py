from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.user_register, name='register'),
    path('verify/<str:token>/', views.verify_email, name='verify_email'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]

