from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

EMOJI_LEVEL = (
    ('light', 'Light'),
    ('medium', 'Medium'),
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
    tone = models.CharField(
        max_length=100,
        choices = TONE, 
        default=TONE[0][0]
        )
    
    emoji_level = models.CharField(
        max_length=100,
        choices=EMOJI_LEVEL,
        default=EMOJI_LEVEL[0][0]
    )
    preferred_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.preferred_name} ({self.user.username})"
    
class Entry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    response = models.CharField(max_length=5000)
    prompt = models.CharField(max_length=500)
    notes = models.CharField(max_length=500, blank=True)
    date = models.DateField()


    def __str__(self):
        return f"{self.user.username} - {self.date}"

class Chat(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True)
    entries= models.ManyToManyField(Entry)
    

    def __str__(self):
        return self.title
    

    