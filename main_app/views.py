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

SAD_KWS= ['sad', 'crying', 'overwhelmed', 'down','lost','stuck', 'bad day', 'help', 'anxious']
GREETING_KWS=['hello', 'hi', 'hey','yo', 'sup', 'whats up', 'greetings']
EXCITED_KWS= ['excited', 'yay', 'great', 'good news', 'omg', 'stoked', 'pumped', 'woohoo', 'win', 'celebrate']
LOVE_KWS= ['love', 'care', 'connection', 'romance', 'feel close', 'miss you', 'heart', 'adore' ]
AWE_KWS=['stars', 'light', 'moon', 'cosmic', 'nature', 'sunrise', 'magic', 'intuitive', 'spirit', 'bright', 'universe', 'sky' ]
META_KWS=['ai', 'robot', 'fake', 'are you real', 'chatbot', 'void', 'sentient', 'this is cool', 'this is so cool' ]
PLAY_KWS=['test', 'testing', 'just checking', 'testtest', 'idk what to say', 'trying this']
ANGER_KWS=['mad', 'angry', 'pissed', 'upset', 'ugh', 'annoyed', 'irate', 'irritated', 'rage']
SWEAR_KW=['damn', 'damn it', 'fuck', 'shit', 'pissed']


#cold and  rainy homework / fizzbuzz 
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


def fake_response(tone, emoji_level, message): 
    message = message.lower()
    if any(word in message for word in SAD_KWS): 
        if tone == 'friendly': 
            if emoji_level == 'no': 
                return "That's really rough. I'm really glad you shared it though. I'm always here for you"
            elif emoji_level == 'robust': 
                return "I see you 🥺💔 It’s okay to let it out 💧"
        elif tone == 'blunt': 
            if emoji_level == 'no': 
                return "woof" 
            elif emoji_level == 'robust': 
                return "🪨 woof 🪨 "
        elif tone == 'cosmic': 
            if emoji_level == 'no':
                return "just remember that you are the universe experiencing itself" 
            elif emoji_level == 'robust': 
                return "yeah, but You are the universe experiencing itself. 🌠🌙💫🪐🌌✨🔮🌞🌜⭐️"
    elif any(word in message for word in GREETING_KWS): 
        if tone == 'friendly': 
            if emoji_level == 'no':
                return "Hi there! So glad you stopped by. (tip: next time, skip the greeting to get something new)"
            elif emoji_level == 'robust':
                return "Yay you're here!! 😊✨ Let’s dive in (psst... skip the 'hi' next time for a different response)"
        elif tone == 'blunt':
            if emoji_level == 'no':
                return "Hello. FYI - if you're looking for variety, drop the greeting next time "
            elif emoji_level == 'robust':
                return "Hey, you're here. 🔊. Next time skip the intro for a real response 😐"
        elif tone == 'cosmic': 
            if emoji_level == 'no': 
                return "Hello, traveler. Speak your truth. (Skip the salutation next time to go deeper)"
            if emoji_level == 'robust': 
                return "Ahh, let's look beyond the veil 🌀🌙. Speak freely now, no need for hello. "
                


            
class ChatCreate(LoginRequiredMixin, CreateView):
    model = Chat 
    fields = ['initial_message', 'tone', 'emoji_level']


    def form_valid(self, form):
        form.instance.user = self.request.user 
        chat = form.save()
        response = fake_response(chat.tone, chat.emoji_level, chat.initial_message)

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
        form.instance.user = self.request.user #logged in user assigned to chat 
        chat = form.save()
        response = fake_response(chat.tone, chat.emoji_level, chat.initial_message) # enter hardcoded response

        entry= chat.entries.first() #first entry connected to this chat. chat = what user types in, entry = ai reply 
        #the first is necessary because i current have chat and entry as one to many but its actually one to one...maybe i will change this....so first is not necessary. 
        entry.response = response #fake response 
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

