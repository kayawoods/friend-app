from django.shortcuts import render
from django.http import HttpResponse 
from django.contrib.auth.views import LoginView



class Home(LoginView):
    template_name = 'home.html'

def about(request): 
    return render(request, 'about.html')

def chat_index(request):
    return render(request, 'chats/index.html')