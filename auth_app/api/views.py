
from auth_app.api.serializers import RegestrationSerializer, LoginSerializer
from rest_framework import status
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

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
                    "user_id" : auth_user.id
                  }
                  
                  return Response(data, status=status.HTTP_200_OK)
            else:
                 data = serializer.errors
            return Response(data, status=status.HTTP_400_BAD_REQUEST)