from django.urls import path
from .views import RegestrationView, LoginView

urlpatterns = [
    path("login/", LoginView.as_view()),
    path("registration/", RegestrationView.as_view(), name="registration")
]