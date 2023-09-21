from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Pet
from .serializers import PetSerializer
from django.http import HttpResponse

def home(request):
    return HttpResponse('Welcome to the Pet Adoption API.')


class PetViewSet(viewsets.ModelViewSet):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .user_serializers import UserSerializer

@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = User.objects.create_user(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password'],
            email=serializer.validated_data['email']
        )
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        return Response(UserSerializer(user).data)
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
