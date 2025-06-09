from django.db import models
from django.contrib.auth.models import User
import uuid

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
    email_token = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return f'Id: {self.user.pk} | {self.user.username}' 
    
    def delete(self, *args, **kwargs):
        self.user.delete()
        super().delete(*args, **kwargs)

class Video(models.Model):
    headline = models.CharField(max_length=50)
    discretion = models.TextField()
    genre = models.CharField(choices=GENRE_CHOICES, default="customer", max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)
    thumbnail = models.FileField(upload_to="uploads/thumbnails", blank=True)
    original_file = models.FileField(upload_to="uploads/videos/originals")

    def __str__(self):
        return f'Id: {self.pk} | HeadLine: {self.headline} |  Genre:{self.genre} | created at: {self.created_at}' 

class VideoFile(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='files')
    resolution = models.CharField(max_length=10)
    file = models.FileField(upload_to="uploads/videos/converted")