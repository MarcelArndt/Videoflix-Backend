from rest_framework import serializers
from service_app.models import Video, Profiles, VideoProgress

class VideosSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Video
        fields = '__all__'


class VideoProgressSerializer(serializers.ModelSerializer):

    class Meta:
        model = VideoProgress
        fields = '__all__'
        read_only_fields = ['profile']


class ProfilesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profiles
        fields = '__all__'
