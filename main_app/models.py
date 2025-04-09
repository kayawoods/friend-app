from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

EMOJI_LEVEL = (
    ('none', 'None'),
    ('light', 'Light'),
    ('heavy', 'Heavy')
)

TONE = (
    ('friendly', 'Friendly'),
    ('stoic', 'Stoic'), 
    ('very honest', 'Very Honest'),
    ('sweet', 'Sweet'),
    ('dry', 'Dry')
)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    preferred_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.preferred_name} ({self.user.username})"
    
class Entry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    response = models.CharField(max_length=5000)
    prompt = models.CharField(max_length=500)
    notes = models.CharField(max_length=500, blank=True)
    date = models.DateField()
    tone = models.CharField(max_length=100, choices=TONE, default='friendly')
    emoji_level = models.CharField(max_length=100, choices=EMOJI_LEVEL, default='light')


    def __str__(self):
        return f"{self.user.username} - {self.date}"

class Chat(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    initial_message = models.TextField()
    entries= models.ManyToManyField(Entry)
    tone = models.CharField(max_length=100, choices=TONE, default='friendly')
    emoji_level = models.CharField(max_length=100, choices=EMOJI_LEVEL, default='light')

    def get_absolute_url(self):
        return reverse('chat-detail', kwargs={'chat_id': self.id})
    

    def __str__(self):
        return f"chat with {self.user.username}"
    

    