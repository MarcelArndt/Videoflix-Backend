
from auth_app.api.serializers import RegestrationSerializer, SendEmailForResetPasswordSerializer, ResetPasswordSerializer, ResetValidationEmailSerializer, EmailTokenObtainSerializer, UserIsAuthenticadeAndVerified
from rest_framework import status
from rest_framework.views import APIView 
from rest_framework.response import Response
from service_app.models import Profiles
from django.http import HttpResponseRedirect
from dotenv import load_dotenv
from rest_framework import status
import os
load_dotenv()
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)
from datetime import datetime, timedelta
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from auth_app.auth import CookieJWTAuthentication

#SECURE = os.environ.get('SECURE', default=False),
SECURE = True

class RegestrationView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = RegestrationSerializer(data= request.data)
        if serializer.is_valid():
            saved_user = serializer.save()
            data = {
                "username": saved_user.user.username,
                "email": saved_user.user.email,
                "user_id": saved_user.id
            }
        else:
            data = serializer.errors
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        return Response(data, status=status.HTTP_201_CREATED)
    
class CookieTokenLogoutView(APIView):
    def post(self, request, *args, **kwargs):
        response = Response({'ok': True},status=status.HTTP_200_OK)
        expires = datetime.now() - timedelta(days=1)
        print('reset Cookie')

        response.set_cookie(
            key = 'access_key',
            value = '',
            expires = expires,
            httponly = True,
            secure = SECURE,
            samesite='Lax'
        )

        response.set_cookie(
            key = 'refresh_key',
            value = '',
            httponly = True,
            expires = expires,
            secure = SECURE,
            samesite='Lax'
        )

        return response
    

class CookieTokenObtainView(TokenObtainPairView):

    serializer_class = EmailTokenObtainSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception = True)

        print(serializer.validated_data)

        refresh = serializer.validated_data['refresh']
        access = serializer.validated_data['access']
        expires = datetime.now() + timedelta(days=7)
        response = Response({'ok':True},status=status.HTTP_200_OK)

        response.set_cookie(
            key = 'access_key',
            value = str(access),
            httponly = True,
            expires=expires,
            secure = SECURE,
            samesite='Lax'
        )

        response.set_cookie(
            key = 'refresh_key',
            expires=expires,
            value = str(refresh),
            httponly = True,
            secure = SECURE,
            samesite='Lax'
        )

        return response
    
class CookieTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_key')
        print(f"Refresh Token for Refresh: {refresh_token}")
        if not refresh_token:
            return Response({'ok':False}, status=status.HTTP_400_BAD_REQUEST)            
        serializer = self.get_serializer(data={'refresh':refresh_token})
        try:
            serializer.is_valid(raise_exception=True)
        except:
            return Response({'ok':False},status=status.HTTP_401_UNAUTHORIZED)

        access_token = serializer.validated_data.get('access')

        response = Response({'ok':True},status=status.HTTP_201_CREATED)
        response.set_cookie(
            key = 'access_key',
            value = str(access_token),
            httponly = True,
            secure = SECURE,
            samesite='Lax'
        )
        return response
    
    
class CookieIsAuthenticatedAndVerifiedView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]

    def post(self, request):
        serializer = UserIsAuthenticadeAndVerified(instance=request.user, context={'request': request})
        return Response(serializer.data)
    

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
    
class ResendEmailView(APIView):
    def post(self, request):
        serializer = ResetValidationEmailSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)