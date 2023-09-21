from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db.models import Q

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Pet, Comment
from .serializers import PetSerializer, CommentSerializer
from .user_serializers import UserSerializer

def home(request):
    return HttpResponse('Welcome to the Pet Adoption API.')

class PetViewSet(viewsets.ModelViewSet):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

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

class PetViewSet(viewsets.ModelViewSet):
    serializer_class = PetSerializer

    def get_queryset(self):
        queryset = Pet.objects.all()

        location = self.request.query_params.get('location', None)
        traits = self.request.query_params.get('traits', None)
        gender = self.request.query_params.get('gender', None)

        if location:
            queryset = queryset.filter(location__icontains=location)
        
        if traits:
            trait_list = traits.split(',')
            query = Q()
            for trait in trait_list:
                query |= Q(personality_traits__icontains=trait)
            queryset = queryset.filter(query)

        if gender:
            queryset = queryset.filter(gender__iexact=gender)

        return queryset