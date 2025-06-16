from rest_framework import generics
from service_app.models import Video, Profiles
from rest_framework.views import APIView
from .serializers import ProfilesSerializer, VideosSerializer
from django.shortcuts import redirect
from django.contrib import messages
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache

class ProfilesListView(generics.ListAPIView):
    queryset = Profiles.objects.all()
    serializer_class = ProfilesSerializer

class ProfilesDetailView(generics.RetrieveAPIView):
    queryset = Profiles.objects.all()
    serializer_class = ProfilesSerializer

class VideosListView(APIView):

    def get(self, request):

        cache_key = 'video_list_view'
        cached_response = cache.get(cache_key)

        if cached_response:
            return Response(cached_response)

        videos = Video.objects.prefetch_related('files').all()
        serialized = VideosSerializer(videos, many=True, context={'request': request}).data
        newest = videos.order_by('-created_at')[:10]
        grouped = {}
        grouped['newOnVideoflix'] = {
            'title': 'New On Videoflix',
            'content': VideosSerializer(newest, many=True, context={'request': request}).data
        }
        for item in serialized:
            genre = item['genre']
            if genre not in grouped:
                grouped[genre] = {
                    'title': genre.capitalize(),
                    'content': []
                }
            grouped[genre]['content'].append(item)
        cache.set(cache_key, grouped, timeout=600)
        return Response(grouped)
    
    def post(self, request):
        serializer = VideosSerializer(data= request.data, context={'request': request})
        if serializer.is_valid():
            cache.delete("video_list_view")
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VideosDetailView(generics.RetrieveDestroyAPIView):
    queryset = Video.objects.all()
    serializer_class = VideosSerializer