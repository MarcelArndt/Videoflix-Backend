from django.urls import path
from .views import ProfilesDetailView, ProfilesListView, VideosDetailView, VideosListView
urlpatterns = [
    path("media/", VideosListView.as_view(), name="media_list"),
    path("media/<int:pk>/", VideosDetailView.as_view(), name="media_detail"),
    path("profiles/", ProfilesListView.as_view(), name="profile_list"),
    path("profiles/<int:pk>/", ProfilesDetailView.as_view(), name="profile_detail"),
]