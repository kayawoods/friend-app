from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from .models import Entry, Profile, Chat 
from django.shortcuts import redirect 
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from datetime import date

@login_required
def chat_index(request):
    print("Current user:", request.user)
    chats = Chat.objects.filter(user=request.user)
    return render(request,'chats/index.html', {'chats': chats})

class Home(LoginView):
    template_name = 'home.html'

def about(request): 
    return render(request, 'about.html')

 
@login_required
def chat(request): 
     user = request.user 
     chat = Chat.objects.create(user = user, initial_message="new chat")
     return redirect('chat-detail', chat_id=chat.id)

@login_required
def chat_detail(request, chat_id):
    chat = Chat.objects.get(id=chat_id)
    entries = chat.entries.all()
    return render(request, 'chats/detail.html', {'chat': chat, 'entries': entries})


def fake_response(tone, emoji_level): 
    return f"I am hardcoded.I am being {tone} with {emoji_level} emojis." 

class ChatCreate(LoginRequiredMixin, CreateView):
    model = Chat 
    fields = ['initial_message', 'tone', 'emoji_level']


    def form_valid(self, form):
        form.instance.user = self.request.user 
        chat = form.save()
        response = fake_response(chat.tone, chat.emoji_level)

        entry= Entry.objects.create(
        user=self.request.user, 
        prompt=chat.initial_message, 
        response = response, 
        date=date.today(),
        tone=chat.tone, 
        emoji_level=chat.emoji_level)

        chat.entries.add(entry)
        return super().form_valid(form)

class ChatUpdate(LoginRequiredMixin, UpdateView):
    model = Chat
    fields = ['tone', 'emoji_level']
    

    def form_valid(self, form): 
        form.instance.user = self.request.user 
        chat = form.save()
        response = fake_response(chat.tone, chat.emoji_level)

        entry= chat.entries.first()
        entry.response = response 
        entry.tone=chat.tone
        entry.emoji_level=chat.emoji_level
        entry.save()

        return super().form_valid(form) 
        

class ChatDelete(LoginRequiredMixin, DeleteView):
    model = Chat
    success_url = '/chats/'   
    
def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('chat-index')
        else:
            error_message = 'Invalid sign up - try again'
    else: 
            form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)

