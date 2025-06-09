
from auth_app.api.serializers import RegestrationSerializer, LoginSerializer, SendEmailForResetPasswordSerializer, ResetPasswordSerializer
from rest_framework import status
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from service_app.models import Profiles
from django.http import HttpResponseRedirect
from dotenv import load_dotenv
import os
load_dotenv()

class RegestrationView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = RegestrationSerializer(data= request.data)
        if serializer.is_valid():
            saved_user = serializer.save()
            token, create = Token.objects.get_or_create(user = saved_user.user)
            data = {
                "token": token.key,
                "username": saved_user.user.username,
                "email": saved_user.user.email,
                "user_id": saved_user.id
            }
        else:
            data = serializer.errors
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        return Response(data, status=status.HTTP_201_CREATED)

class LoginView(ObtainAuthToken):
        def post(self, request, *args, **kwargs):
            serializer = LoginSerializer(data=request.data)
            if serializer.is_valid():
                  auth_user = serializer.validated_data["user_profile"]
                  token, create = Token.objects.get_or_create(user = auth_user.user)
                  data = {
                    "username" : auth_user.user.username,
                    "email" : auth_user.user.email,
                    "token" : token.key,
                    "user_id" : auth_user.id,
                    "email_is_confirmed" : auth_user.email_is_confirmed
                  }
                  
                  return Response(data, status=status.HTTP_200_OK)
            else:
                 data = serializer.errors
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

class VerifyEmailView(APIView):
    def get(self, request):
        token = request.GET.get('token')
        url = os.environ.get('URL_FOR_VERIFY_USER')
        try:
            user = Profiles.objects.get(email_token=token)
            user.email_is_confirmed = True
            user.save()
        except Profiles.DoesNotExist:
            pass
        finally:
            return HttpResponseRedirect(url)



class SendEmailForResetPasswordView(APIView):
    def post(self, request):
        serializer = SendEmailForResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class SetNewPasswordView(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)