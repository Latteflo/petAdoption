# user_viewset.py
from rest_framework import viewsets, status
from rest_framework.decorators import action, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from ..models import Comment, Like, Pet, Shelter
from ..serializers import UserSerializer, CommentSerializer, LikeSerializer, PetSerializer, ShelterSerializer
from django.contrib.auth import authenticate
from rest_framework.authentication import SessionAuthentication

class UserViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    # Custom action for User's Registration
    @action(detail=False, methods=['POST'], url_path='register')
    def register(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(
                username=serializer.validated_data['username'],
                last_name=serializer.validated_data['last_name'],
                first_name=serializer.validated_data['first_name'],
                location=serializer.validated_data['location'],
                password=serializer.validated_data['password'],
                email=serializer.validated_data['email']
            )
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Custom action for User's Login
    @action(detail=False, methods=['POST'], url_path='login')
    def login(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            return Response(UserSerializer(user).data)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
    
  # Custom action for User's Comments
    @action(detail=True, methods=['GET', 'POST'], permission_classes=[IsAuthenticated])
    def comments(self, request, pk=None):
        if request.method == 'GET':
            comments = Comment.objects.filter(user=pk)
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data)
        elif request.method == 'POST':
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user_id=pk)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Custom action for User's Likes
    @action(detail=True, methods=['GET', 'POST'], permission_classes=[IsAuthenticated])
    def likes(self, request, pk=None):
        if request.method == 'GET':
            likes = Like.objects.filter(user=pk)
            serializer = LikeSerializer(likes, many=True)
            return Response(serializer.data)
        elif request.method == 'POST':
            serializer = LikeSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user_id=pk)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Custom action for User's Pets
    @action(detail=True, methods=['GET', 'POST'], permission_classes=[IsAuthenticated])
    def pets(self, request, pk=None):
        if request.method == 'GET':
            pets = Pet.objects.filter(user=pk)
            serializer = PetSerializer(pets, many=True)
            return Response(serializer.data)
        elif request.method == 'POST':
            serializer = PetSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user_id=pk)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Custom action for User's Shelters
    @action(detail=True, methods=['GET', 'POST'], permission_classes=[IsAuthenticated])
    def shelters(self, request, pk=None):
        if request.method == 'GET':
            shelters = Shelter.objects.filter(user=pk)
            serializer = ShelterSerializer(shelters, many=True)
            return Response(serializer.data)
        elif request.method == 'POST':
            serializer = ShelterSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user_id=pk)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)