from rest_framework import serializers
from service_app.models import Video, Profiles

class VideosSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Video
        fields = '__all__'





class ProfilesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profiles
        fields = '__all__'
