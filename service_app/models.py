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
    email_is_confirmed = models.BooleanField(default=False)

class Video(models.Model):
    headline = models.CharField(max_length=50)
    discretion = models.TextField()
    genre = models.CharField(choices=GENRE_CHOICES, default="customer", max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)
    thumbnail = models.FileField(upload_to="uploads/thumbnails", blank=True)
    original_file = models.FileField(upload_to="uploads/videos/originals")

class VideoFile(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='files')
    resolution = models.CharField(max_length=10)
    file = models.FileField(upload_to="uploads/videos/converted")