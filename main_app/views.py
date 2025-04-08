from django.shortcuts import render
from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from .models import Entry, Profile, Chat 
from django.shortcuts import redirect 
from django.views.generic.edit import CreateView


def chat_index(request):
    print("Current user:", request.user)
    chats = Chat.objects.filter(user=request.user)
    return render(request,'chats/index.html', {'chats': chats})

class Home(LoginView):
    template_name = 'home.html'

def about(request): 
    return render(request, 'about.html')

 
def chat(request): 
     user = request.user 
     chat = Chat.objects.create(user = user, initial_message="new chat")
     return redirect('chat-detail', chat_id=chat.id)

def chat_detail(request, chat_id):
    chat = Chat.objects.get(id=chat_id)
    entries = chat.entries.all()
    return render(request, 'chats/detail.html', {'chat': chat, 'entries': entries})


def fake_response(tone, emoji_level): 
    return f"I am hardcoded.I am being {tone} with {emoji_level} emojis." 

class ChatCreate(CreateView):
    model = Chat 
    fields = ['initial_message', 'tone', 'emoji_level']


    def form_valid(self,form): 
        form.instance.user = self.request.user
        return super().form_valid(form)
    
