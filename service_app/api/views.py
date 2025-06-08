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

class VideosListView(generics.ListCreateAPIView):
    queryset = Video.objects.all()
    serializer_class = VideosSerializer

class VideosDetailView(generics.RetrieveDestroyAPIView):
    queryset = Video.objects.all()
    serializer_class = VideosSerializer


class VerifyEmailView(APIView):
    def get(self, request):
        token = request.GET.get('token')
        try:
            user = Profiles.objects.get(email_token=token)
            user.email_is_confirmed = True
            user.save()
            return Response({'message': 'E-Mail bestätigt!'}, status=status.HTTP_200_OK)
        except Profiles.DoesNotExist:
            return Response({'error': 'Token ungültig'}, status=status.HTTP_400_BAD_REQUEST)