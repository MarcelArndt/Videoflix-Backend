from django.urls import path
from .views import RegestrationView, LoginView, VerifyEmailView, SendEmailForResetPasswordView, SetNewPasswordView

urlpatterns = [
    path("login/", LoginView.as_view(), name='login'),
    path("registration/", RegestrationView.as_view(), name="registration"),
    path('verify-email/', VerifyEmailView.as_view(), name='verify_email'),
    path('find-user/', SendEmailForResetPasswordView.as_view(), name='find_user_reset'),
    path('password_reset/', SetNewPasswordView.as_view(), name='password_reset'),
]