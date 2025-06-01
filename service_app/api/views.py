from rest_framework import generics
from service_app.models import Videos, Profiles
from .serializers import ProfilesSerializer, VideosSerializer

class ProfilesListView(generics.ListAPIView):
    queryset = Profiles.objects.all()
    serializer_class = ProfilesSerializer

class ProfilesDetailView(generics.RetrieveAPIView):
    queryset = Profiles.objects.all()
    serializer_class = ProfilesSerializer

class VideosListView(generics.ListCreateAPIView):
    queryset = Videos.objects.all()
    serializer_class = VideosSerializer

class VideosDetailView(generics.RetrieveAPIView):
    queryset = Videos.objects.all()
    serializer_class = VideosSerializer