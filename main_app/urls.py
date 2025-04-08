from django.urls import path 
from . import views 

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('chats/', views.chat_index, name='chat-index'), 
    path('chats/<int:chat_id>/',views.chat_detail, name='chat_detail'), 
    path('chat/', views.chat, name='chat')
]