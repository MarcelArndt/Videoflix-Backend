from django.db import models
from django.contrib.auth.models import User

GENRE_CHOICES = [
    ("crime", "Crime"),
    ("romance", "Romance"),
    ("drama", "Drama"),
    ("comedy", "Comedy"),
    ("horror", "Horror"),
    ("documentation", "Documentation"),
    ('adventure','Adventure')    
    ]

class Profiles(models.Model):
    user = models.OneToOneField(User, verbose_name=("User"), on_delete=models.CASCADE, related_name="abstract_user")

class Videos(models.Model):
    headline = models.CharField(max_length=50, blank=True)
    discretion = models.TextField(blank=True)
    video = models.FileField(upload_to="uploads/videos", blank=True)
    genre = models.CharField(choices=GENRE_CHOICES, default="customer", max_length=25, blank=True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    thumbnail = models.FileField(upload_to="uploads/thumbnails")

