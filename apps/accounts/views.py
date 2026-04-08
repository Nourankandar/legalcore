from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import UserSerializer,RegisterSerializer


class RegisterView(APIView):
    def post(self,request):
        serializer = RegisterSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(UserSerializer(user).data, status=201)


class MyProfileView(APIView):
    permission_classes =[IsAuthenticated]
    
    def get(self,request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
