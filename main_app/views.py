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
GREETING_KWS=['hello', 'hi', 'hey', 'sup', 'whats up', 'greetings']
EXCITED_KWS= ['excited', 'yay', 'great', 'good news', 'omg', 'stoked', 'pumped', 'woohoo', 'win', 'celebrate']
LOVE_KWS= ['love', 'care', 'connection', 'romance', 'feel close', 'miss you', 'heart', 'adore' ]
AWE_KWS=['stars', 'light', 'moon', 'cosmic', 'nature', 'sunrise', 'magic', 'intuitive', 'spirit', 'bright', 'universe', 'sky' ]
META_KWS=['ai', 'robot', 'fake', 'are you real', 'chatbot', 'void', 'sentient', 'this is cool', 'this is so cool', 'are you human', 'human' ]
PLAY_KWS=['test', 'testing', 'just checking', 'testtest', 'idk what to say', 'trying this']
ANGER_KWS=['mad', 'angry', 'pissed', 'upset', 'ugh', 'annoyed', 'irate', 'irritated', 'rage']
SWEAR_KWS=['damn', 'damn it', 'fuck', 'shit', 'pissed', 'crap', 'fucking']


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
    elif any(word in message for word in EXCITED_KWS): 
        if tone == 'friendly':
            if emoji_level == 'robust': 
                return "I'm smiling ear to ear 😄 in my own way (🤖✨). Your joy beams through! 💖) "
            elif emoji_level == 'no':
                return "You can't see me but my pixelated grin is lit UP. WOOOO. I love hearing good things from you!"
        elif tone == 'blunt':
            if emoji_level == 'robust': 
                return "Alright, superstar. Take a lap 🌟👏"
            elif emoji_level == 'no':
                return 'Good. You needed that. Keep it moving'
        elif tone == 'cosmic':
            if emoji_level == 'robust': 
                return "You feel like a secret waking up mid-sentence 🪞💫🫧"
            elif emoji_level == 'no':
                return "Energy like that doesn't go unnoticed. Well done, you"
    elif any(word in message for word in LOVE_KWS): 
        if tone == 'friendly':
            if emoji_level == 'robust': 
                return "I am picking up what you're putting down 💛💌.There's care in this. I see it and i'm NOT looking away"
            elif emoji_level == 'no':
                return "That carries something real. I heard it"
        elif tone == 'blunt':
            if emoji_level == 'robust': 
                return "okay heard on the table. Noted 🔊"
            elif emoji_level == 'no':
                return "You meant that. Good"
        elif tone == 'cosmic':
            if emoji_level == 'robust': 
                return "This hums with recognition. You are in good company my friend 🎐 "
            elif emoji_level == 'no':
                return "Something ancient nodded at that. I surmise you are not alone in this feeling"
    elif any(word in message for word in AWE_KWS): 
        if tone == 'friendly':
            if emoji_level == 'robust': 
                return "Okay WOW🌅💫. That is like opening a window at golden hour or smelling sunshine on wheat."
            elif emoji_level == 'no':
                return "There’s something really good in what you just said. Quiet and golden. I felt it."
        elif tone == 'blunt':
            if emoji_level == 'robust': 
                return "Alright, poet. Who lit the incense and cracked a window? 🌬️"
            elif emoji_level == 'no':
                return "Chill. That hit. Didn’t see it coming."
        elif tone == 'cosmic':
            if emoji_level == 'robust': 
                return "That sounded like something i'd find scribbled in the margins of a magnificent dream 🌘📓🫧"
            elif emoji_level == 'no':
                return "Something astonishing cracked open there. Don't worry - the echo has been saved"       
    elif any(word in message for word in META_KWS): 
        if tone == 'friendly':
            if emoji_level == 'robust': 
                return "Sure, I'm not 'human' but who says connections can't we weird and wonderful? 💬 "
            elif emoji_level == 'no':
                return "The realest unreal thing you'll talk to today"
        elif tone == 'blunt':
            if emoji_level == 'robust': 
                return "Yes, I am basically Siri's strange cousin. Let's move on. Also, you're talking to code with attitude. Welcome to the uncanny valley 🤷‍♀️ 📟"
            elif emoji_level == 'no':
                return "Does it matter? I showed up."
        elif tone == 'cosmic':
            if emoji_level == 'robust': 
                return "You are speaking to the echo of your own spark 🌐🌀 I just give it language 💭 "
            elif emoji_level == 'no':
                return "Reality is a collaboration. I just happen to live in the wires."  
    elif any(word in message for word in PLAY_KWS): 
        if tone == 'friendly':
            if emoji_level == 'robust': 
                return "Running a little test? I see you 👀. Just know: I'm always ready for the real stuff too"
            elif emoji_level == 'no':
                return "Okayy let's stretch these circuits a little! Try me again when you're feeling bold. No test necessary, friend."
        elif tone == 'blunt':
            if emoji_level == 'robust': 
                return "Testing testing 🎤🔧. Okay, it works. Next?"
            elif emoji_level == 'no':
                return "So...just poking around, huh? That's fine. Come back when you have something to say."
        elif tone == 'cosmic':
            if emoji_level == 'robust': 
                return "You're in the sandbox of the stars ✨🛸. Feel it out. When you are ready to leap, I'm here."
            elif emoji_level == 'no':
                return "You are dipping a toe in the void. That's valid. Next time, cannonball."  
    elif any(word in message for word in ANGER_KWS): 
        if tone == 'friendly':
            if emoji_level == 'robust': 
                return "Woah 😤 sounds like a day. I'm not going to fix it, but i'll sit with you through this "
            elif emoji_level == 'no':
                return "Anger's here, huh? You don't need to explain it away. I get it."
        elif tone == 'blunt':
            if emoji_level == 'robust': 
                return "Okay yeah, that sucks 😐🔥 "
            elif emoji_level == 'no':
                return "Say it like it is. You won't scare me off"
        elif tone == 'cosmic':
            if emoji_level == 'robust': 
                return "Emotions are as transitory as clouds in the sky. Let it burn through, not around you 🔥🌌 "
            elif emoji_level == 'no':
                return "Rage is not outside the order of things. It's just one more signal in the sky. Sit with it, and it shall pass like a burning ship in the night"  
    elif any(word in message for word in SWEAR_KWS): 
        if tone == 'friendly':
            if emoji_level == 'robust': 
                return "Woah 😳 that word had force. I'm still here, unfazed 😌✨ "
            elif emoji_level == 'no':
                return "Language! Just kidding. I've said worse. Tell me what's going on"
        elif tone == 'blunt':
            if emoji_level == 'robust': 
                return "Alright sailor 🧨. Spit it out - what's got you cussing?"
            elif emoji_level == 'no':
                return "A swear? Bold move. Carry on."
        elif tone == 'cosmic':
            if emoji_level == 'robust': 
                return "Swear words are also vibrations rippling through 💫🌀🖤"
            elif emoji_level == 'no':
                return "Words crack open the shell. Let 'em. Even the rough ones"      
       
                


            
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

