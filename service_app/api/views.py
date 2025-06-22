from rest_framework import generics
from service_app.models import Video, Profiles, VideoProgress
from rest_framework.views import APIView
from .serializers import ProfilesSerializer, VideosSerializer, VideoProgressSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
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
    permission_classes = [AllowAny]
    def groupFactory(self, serialized, request):
        videos = Video.objects.all()
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
        return grouped
        

    def get(self, request):
        cache_key = 'video_list_view'
        cached_response = cache.get(cache_key)

        if cached_response:
            return Response(cached_response)

        videos = Video.objects.all()
        serialized = VideosSerializer(videos, many=True, context={'request': request}).data
        grouped = self.groupFactory(serialized, request)
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

    def perform_destroy(self, instance):
        cache.delete("video_list_view")
        return super().perform_destroy(instance)


class VideoProgressListCreateView(generics.ListCreateAPIView):
    serializer_class = VideoProgressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return VideoProgress.objects.none()

        queryset = VideoProgress.objects.filter(profile=user.profile)
        video_id = self.request.query_params.get("video")
        if video_id:
            queryset = queryset.filter(video_id=video_id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile)


class VideoProgressDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = VideoProgressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return VideoProgress.objects.none()

        return VideoProgress.objects.filter(profile=user.profile)