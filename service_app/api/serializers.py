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
        extra_kwargs = {
            'profiles': {'write_only': True,'required': False},
            'current_time': {'required': False},
        }
    
    def validate(self, data):
        video = data.get('video')
        if video is None:
            raise serializers.ValidationError({"error": "Video not found."})
        data['current_time'] = data.get('current_time') or 0
        data['is_finished'] = data.get('is_finished') or False
        return data

    def create(self, validated_data):
        return super().create(validated_data)


class ProfilesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profiles
        fields = '__all__'
