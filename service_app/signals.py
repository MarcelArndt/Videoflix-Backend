import os
import subprocess
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Video, VideoFile
from django.conf import settings
from django.core.files.base import ContentFile

RESOLUTIONS = {
        'videos': {
            '1080p': '1920x1080',
            '720p': '1280x720',
            '480p': '854x480',
            '360p': '640x360',
        },
        'thumbnails': '215:120'
    }


@receiver(post_save, sender=Video)
def generate_video_data(sender, instance, created, **kwargs):
    if not created or not instance.original_file:
        return
    generate_video_thumbnail(instance)
    generate_video_versions(instance)


def generate_video_versions(instance):
    output_dir = os.path.join(settings.MEDIA_ROOT, 'uploads/videos/converted')
    os.makedirs(output_dir, exist_ok=True)
    
    video = instance.original_file.path
    filename, ending = os.path.splitext(os.path.basename(video))

    for resolution, size in RESOLUTIONS['videos'].items():
        output_path = os.path.join(settings.MEDIA_ROOT, 'uploads/videos/converted', f'{filename}_{resolution}{ending}')
        cmd = ['ffmpeg', '-i', video, '-vf', f'scale={size}', '-c:v', 'libx264', '-crf', '23', '-preset', 'medium', output_path]
        try:
            subprocess.run(cmd, check=True)
            VideoFile.objects.create(video=instance, resolution=resolution, file=output_path)
        except subprocess.CalledProcessError as error:
            print(f"[ffmpeg] Fehler bei {resolution}: {error}")


def generate_video_thumbnail(instance):
    video = instance.original_file.path
    output_dir = os.path.join(settings.MEDIA_ROOT, 'uploads/thumbnails')
    os.makedirs(output_dir, exist_ok=True)
    name, _ = os.path.splitext(os.path.basename(video))
    thumbnail_path = os.path.join(settings.MEDIA_ROOT, 'uploads/thumbnails', f"{instance.id}_thumb.jpg")
    cmd = ['ffmpeg', '-ss', '00:00:08', '-i', video, '-frames:v', '1', '-vf', f"scale={RESOLUTIONS['thumbnails']}", thumbnail_path ]
    try:
        subprocess.run(cmd, check=True)
        with open(thumbnail_path, 'rb') as image:
            instance.thumbnail.save(f"uploads/thumbnails/{instance.id}_thumb.jpg", ContentFile(image.read()), save=True)
    except subprocess.CalledProcessError as error:
        print(f"[ffmpeg] Fehler bei Thumbnail: {error}")
