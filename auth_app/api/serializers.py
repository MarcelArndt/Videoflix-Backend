from rest_framework import serializers
from service_app.models import Profiles
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from dotenv import load_dotenv
import os

from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

load_dotenv()

class RegestrationSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(write_only = True)
    password = serializers.CharField(write_only = True)
    email = serializers.EmailField(write_only=True)
    username = serializers.CharField(write_only = True)

    class Meta():
        model = Profiles
        fields = ["username", "email", "password", "repeated_password"]
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, data):
        password = data.get("password")
        repeatingPassword = data.get("repeated_password")
        email = data.get("email")
        username = data.get("username")

        if User.objects.filter(username = username).exists():
            raise serializers.ValidationError({'username':"Username already exists."})
        if not repeatingPassword == password:
            raise serializers.ValidationError({'password':"passwords doesn't match"})
        if not email:
            raise serializers.ValidationError({'email':"Email is required."})
        if User.objects.filter(email = email).exists():
            raise serializers.ValidationError({'email':"Email already exists."}) 

        return data

    def create(self, validated_data) :
        password = self.validated_data.get('password')
        email = self.validated_data.get("email")
        username = self.validated_data.get('username')
        user = User.objects.create_user(username = username, email = email, password = password)
        user_profiles = Profiles.objects.create(user = user)
        return user_profiles

class LoginSerializer(serializers.Serializer):
        email = serializers.CharField(write_only=True)
        password = serializers.CharField(write_only=True)

        def validate(self, data):
            email = data.get("email")
            password = data.get("password")
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise serializers.ValidationError({'email': "wrong email"})
            if not user:
                raise serializers.ValidationError({'email':"wrong email"})
            if not user.check_password(password):
                 raise serializers.ValidationError({'password':"wrong password"})
            try:
                user_profile = user.abstract_user
            except:
                raise serializers.ValidationError({'user':"No User found"})
            return {"user_profile" : user_profile}
        
class SendEmailForResetPasswordSerializer(serializers.Serializer):
    email = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        try:
            user = User.objects.get(email=email)
        except:
             raise serializers.ValidationError({'user':"No User found"})
        userId = urlsafe_base64_encode(force_bytes(user.pk))
        token  = default_token_generator.make_token(user)
        username = user.username
        user_email = user.email
        base_url = os.environ.get('URL_FOR_RESET_PASSWORD')
        reset_link = f"{base_url}?user={userId}&token={token}"
        self.send_email_to_user(username, user_email, reset_link)
        return {"user" : 'email in on the way'}

    def send_email_to_user(self, username, user_email, reset_link):
        html_content = render_to_string("emails/reset-password.html", {
            "username": username,
            "reset_link": reset_link,
        })
        text_content = f"Klicke hier, um dein Passwort zurückzusetzen:\n{reset_link}"
        email = EmailMultiAlternatives(
            subject="Reset your Password",
            body=text_content,
            from_email='noreply@videoflix.de',
            to=[user_email],
        )
        email.attach_alternative(html_content, "text/html")
        email.send()

class ResetPasswordSerializer(serializers.Serializer):
    token = serializers.CharField(write_only=True)
    userId = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    repeated_password = serializers.CharField(write_only=True)

    def validate(self, data):
        password = data.get("password")
        repeatingPassword = data.get("repeated_password")
        token = data.get("token")
        userId = data.get("userId")
        try:
            decoded_id = urlsafe_base64_decode(userId)
            user = User.objects.get(pk=decoded_id)
        except:
            raise serializers.ValidationError({'user':"No User found"})
        if not default_token_generator.check_token(user, token):
            raise serializers.ValidationError({'token': "Invalid or expired token"})
        if password != repeatingPassword:
             raise serializers.ValidationError({'password':"Passwords not match"})
        user.set_password(password)
        user.save()
        return {"message": "password successfully reseted"}



    


