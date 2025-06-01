from rest_framework import serializers
from service_app.models import Profiles
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

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
            user = get_object_or_404(User, email=email)
            if not user:
                raise serializers.ValidationError({'email':"wrong email"})

            if not user.check_password(password):
                 raise serializers.ValidationError({'password':"wrong password"})
            try:
                user_profile = user.abstract_user
            except:
                raise serializers.ValidationError({'user':"No User found"})

            return {"user_profile" : user_profile}