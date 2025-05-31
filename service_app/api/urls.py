from django.urls import path
urlpatterns = [
    path("media/", ProfilesListView.as_view(), name="media_list"),
    path("media/<int:pk>/", ProfilesListView.as_view(), name="media_detail"),
    path("profiles/<int:pk>/", ProfilesFilteredListView.as_view(), name="profile_list"),
    path("profiles/", ProfilesFilteredListView.as_view(), name="profile_detail"),
]