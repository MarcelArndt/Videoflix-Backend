from rest_framework import generics
from service_app.models import Video, Profiles
from rest_framework.views import APIView
from .serializers import ProfilesSerializer, VideosSerializer
from django.shortcuts import redirect
from django.contrib import messages
from rest_framework.response import Response
from rest_framework import status

class ProfilesListView(generics.ListAPIView):
    queryset = Profiles.objects.all()
    serializer_class = ProfilesSerializer

class ProfilesDetailView(generics.RetrieveAPIView):
    queryset = Profiles.objects.all()
    serializer_class = ProfilesSerializer

class VideosListView(APIView):

    def get(self, request):
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


        return Response(grouped)
    
    def post(self, request):
        serializer = VideosSerializer(data= request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VideosDetailView(generics.RetrieveDestroyAPIView):
    queryset = Video.objects.all()
    serializer_class = VideosSerializer