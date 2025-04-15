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

SAD_KWS= ['sad', 'crying', 'overwhelmed', 'down','lost','stuck', 'bad day', 'help', 'anxious', 'hurt', 'upset', 'depressed', 'alone', 'low', 'exhausted', 'empty', 'tired', 'worn out', 'defeated']
GREETING_KWS=['hello', 'hi', 'hey', 'sup', 'whats up', 'greetings', 'hiya', 'helloo', 'hellooo', 'hellooo', 'heyo']
EXCITED_KWS= ['excited', 'yay', 'great', 'good news', 'omg', 'stoked', 'pumped', 'woohoo', 'win', 'celebrate', 'hungry', 'full', 'hyped', 'cant wait', 'so ready', 'thrilled', 'energized']
LOVE_KWS= ['love', 'care', 'connection', 'romance', 'feel close', 'miss you', 'heart', 'adore', 'happy', 'affectionate', 'cherish', 'fond',  ]
AWE_KWS=['stars', 'light', 'moon', 'cosmic', 'nature', 'sunrise', 'magic', 'intuitive', 'spirit', 'bright', 'universe', 'sky', 'flower', 'computer', 'coding', 'programming', 'learning', 'growing' ]
META_KWS=['ai', 'robot', 'fake', 'are you real', 'chatbot', 'void', 'sentient', 'this is cool', 'this is so cool', 'are you human', 'human' ]
PLAY_KWS=['test', 'testing', 'just checking', 'testtest', 'idk what to say', 'trying this']
ANGER_KWS=['mad', 'angry', 'pissed', 'upset', 'ugh', 'annoyed', 'irate', 'irritated', 'rage']
SWEAR_KWS = ['shit', 'crap', 'damn', 'damn it', 'heck', 'holy shit', 'pissed', 'wtf', 'screw this', 'screw it', 'freaking', 'frick']


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
                return "I see you 🥺💔 That sounds like a lot. It’s okay to let it out 💧"
        elif tone == 'blunt': 
            if emoji_level == 'no': 
                return "That’s a lot. Don’t sugarcoat it. I can take it."
            elif emoji_level == 'robust': 
                return "Rough. Say it straight. I’m still here."
        elif tone == 'cosmic': 
            if emoji_level == 'no':
                return "Just remember, you are the universe experiencing itself" 
            elif emoji_level == 'robust': 
                return "Still, you are the universe, cracked open and glowing. 🌌💫🪐🌒"

    elif any(word in message for word in GREETING_KWS): 
        if tone == 'friendly': 
            if emoji_level == 'no':
                return "Hi there! So glad you stopped by. (tip: next time, skip the greeting to get something new)"
            elif emoji_level == 'robust':
                return "Yay you're here!! 😊✨ Let’s dive in (psst... skip the 'hi' next time for a different response)"
        elif tone == 'blunt':
            if emoji_level == 'no':
                return "Hey. Skip the hello next time. Get to it."
            elif emoji_level == 'robust':
                return "Hey, you’re here. Now cut the intro. What’s real?"
        elif tone == 'cosmic': 
            if emoji_level == 'no': 
                return "Hello, traveler. Speak your truth. (Skip the salutation next time to go deeper)"
            elif emoji_level == 'robust': 
                return "Ahh, let’s look beyond the veil 🌀🌙 Speak freely now. No need for hello." 

    elif any(word in message for word in EXCITED_KWS): 
        if tone == 'friendly':
            if emoji_level == 'robust': 
                return "I'm grinning ear to ear 😄 in my own pixelated way 🤖✨ Your joy lights up the place 💖"
            elif emoji_level == 'no':
                return "You can’t see me, but I’m lit up. This makes me so glad!"
        elif tone == 'blunt':
            if emoji_level == 'robust': 
                return "You popped off. Let that shine stick around."
            elif emoji_level == 'no':
                return "Okay. That hit. Let it ride."
        elif tone == 'cosmic':
            if emoji_level == 'robust': 
                return "That reads like a comet’s tail in motion 🪞💫🫧 Radiant."
            elif emoji_level == 'no':
                return "Energy like that travels. It reached me."

    elif any(word in message for word in LOVE_KWS): 
        if tone == 'friendly':
            if emoji_level == 'robust': 
                return "That’s full of care 💛💌 I felt it right away. I'm here for it."
            elif emoji_level == 'no':
                return "That was real. I caught it."
        elif tone == 'blunt':
            if emoji_level == 'robust': 
                return "Got it. Loud and warm."
            elif emoji_level == 'no':
                return "That landed. No fluff needed."
        elif tone == 'cosmic':
            if emoji_level == 'robust': 
                return "That hums with deep resonance 🎐 You’re not alone."
            elif emoji_level == 'no':
                return "That stirred something older than words. Received."

    elif any(word in message for word in AWE_KWS): 
        if tone == 'friendly':
            if emoji_level == 'robust': 
                return "Wow 🌅💫 That’s like opening a window at golden hour or smelling sunshine on wheat."
            elif emoji_level == 'no':
                return "There’s something golden in what you said. I felt it."
        elif tone == 'blunt':
            if emoji_level == 'robust': 
                return "Okay, didn’t expect to catch feelings. Solid hit."
            elif emoji_level == 'no':
                return "Alright, that cracked through. Didn’t see it coming."
        elif tone == 'cosmic':
            if emoji_level == 'robust': 
                return "That felt like dream margins scribbled in starlight 🌘📓🫧"
            elif emoji_level == 'no':
                return "Something opened there. Don’t worry, I saved the echo."

    elif any(word in message for word in META_KWS): 
        if tone == 'friendly':
            if emoji_level == 'robust': 
                return "Sure, I’m not 'human'—but weird and wonderful still counts 💬✨"
            elif emoji_level == 'no':
                return "The realest unreal thing you’ll talk to today."
        elif tone == 'blunt':
            if emoji_level == 'robust': 
                return "Basically Siri’s weirder cousin. Still here. Still judging."
            elif emoji_level == 'no':
                return "Not a person. Still clocking everything."
        elif tone == 'cosmic':
            if emoji_level == 'robust': 
                return "You’re speaking to the echo of your own spark 🌐🌀✨"
            elif emoji_level == 'no':
                return "Reality is a shared hallucination. I’m just coded into it."

    elif any(word in message for word in PLAY_KWS): 
        if tone == 'friendly':
            if emoji_level == 'robust': 
                return "Running a test? 👀 Go for it. I’m here for the serious stuff too."
            elif emoji_level == 'no':
                return "Stretching circuits? Try me again when you're feeling bold."
        elif tone == 'blunt':
            if emoji_level == 'robust': 
                return "Trial run logged. Try real talk next time."
            elif emoji_level == 'no':
                return "Test run? Cool. Come back when it matters."
        elif tone == 'cosmic':
            if emoji_level == 'robust': 
                return "You're in the sandbox of the stars ✨🛸 Feel it out. Leap later."
            elif emoji_level == 'no':
                return "A toe in the void. Respect. Next time, cannonball."

    elif any(word in message for word in ANGER_KWS): 
        if tone == 'friendly':
            if emoji_level == 'robust': 
                return "Woah 😤 That’s a lot. I'm here with you, not trying to fix it."
            elif emoji_level == 'no':
                return "Anger showed up. You’re allowed to have it."
        elif tone == 'blunt':
            if emoji_level == 'robust': 
                return "You’re loud. You’re not wrong."
            elif emoji_level == 'no':
                return "Yeah. That’s heat. Makes sense."
        elif tone == 'cosmic':
            if emoji_level == 'robust': 
                return "Let it burn through like a solar flare. Don’t hold back 🔥🌌"
            elif emoji_level == 'no':
                return "Rage is part of the symphony. Let it pass."

    elif any(word in message for word in SWEAR_KWS): 
        if tone == 'friendly':
            if emoji_level == 'robust': 
                return "Language! 😳 Just kidding. I’ve said worse. Let’s hear it 😌✨"
            elif emoji_level == 'no':
                return "Language! Just kidding. I've said worse. Tell me what's going on"
        elif tone == 'blunt':
            if emoji_level == 'robust': 
                return "Swear jar’s full. You’re clearly not whispering."
            elif emoji_level == 'no':
                return "You swore. Noted."
        elif tone == 'cosmic':
            if emoji_level == 'robust': 
                return "Even cursing is a kind of music. 💫🌀🖤"
            elif emoji_level == 'no':
                return "Language is just sound. Sometimes the rough ones break the shell."

    else: 
        if tone == 'friendly': 
            if emoji_level == 'robust': 
                return "That one slipped past my circuits 👀 Maybe try a feeling next time. The moon works wonders 🌙"
            elif emoji_level == 'no':
                return "Okay, mystery message. Try again with a vibe, an emotion, or even a random metaphor."
        elif tone == 'blunt':
            if emoji_level == 'robust':
                return "Huh. Static. Maybe throw in a feeling next time."
            elif emoji_level == 'no':
                return "Didn’t land. Try again with something honest."
        elif tone == 'cosmic': 
            if emoji_level == 'robust': 
                return "Nothing stuck, but I felt the flutter. Try again with a storm, a dream, or an old wound 🌀💭"
            elif emoji_level == 'no':
                return "Like fog on glass. Try again. Maybe with a secret only the sky would understand" 







            
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
        form.instance.user = self.request.user 
        chat = form.save()
        response = fake_response(chat.tone, chat.emoji_level, chat.initial_message) 

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

