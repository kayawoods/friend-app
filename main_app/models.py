from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tone = models.CharField(max_length=100)
    emoji_level = models.CharField(max_length=100)
    preferred_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.preferred_name} ({self.user.username})"
    
class Entry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    response = models.CharField(max_length=5000)
    notes = models.CharField(max_length=500, blank=True)
    date = models.DateField()
    def __str__(self):
        return f"{self.user.username} - {self.date}"
    