from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from ..models import Comment, Like, Pet, Shelter , UserProfile
from ..serializers import UserSerializer, CommentSerializer, LikeSerializer, PetSerializer, ShelterSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            return []
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated()]
        else:
            return []
    
    # Custom action for User's Registration
    @action(detail=False, methods=['POST'], url_path='register')
    def register(self, request):
      """
      Register a new user.
      """
      serializer = UserSerializer(data=request.data)
      if serializer.is_valid():
        username = serializer.validated_data['username']
        email = serializer.validated_data['email']

        # Check if username or email already exists
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=email).exists():
            return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)

        # Create User
        user = User.objects.create_user(
            username=serializer.validated_data['username'],
            last_name=serializer.validated_data['last_name'],
            first_name=serializer.validated_data['first_name'],
            email=serializer.validated_data['email']
        )
        user.set_password(serializer.validated_data['password'])
        user.save()

        # Create or Update UserProfile
        UserProfile.objects.update_or_create(user=user, defaults={
            'location': serializer.validated_data.get('location', ''),
            'image': serializer.validated_data.get('image', '')
        })

        # Create Token
        token = Token.objects.create(user=user)

        return Response({'token': token.key}, status=status.HTTP_201_CREATED)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'], url_path='login')
    def login(self, request):
        """
        Login a user.
        """
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        # Validate that either username or email is provided
        if not username and not email:
            return Response({'error': 'Either username or email must be provided'}, status=status.HTTP_400_BAD_REQUEST)

        # Attempt to retrieve the user
        try:
            user = User.objects.get(username=username) if username else User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'Username or email does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        # Authenticate the user
        user = authenticate(username=user.username, password=password)
        if not user:
            return Response({'error': 'Invalid password'}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve or create token
        token, _ = Token.objects.get_or_create(user=user)

        return Response({'token': token.key}, status=status.HTTP_200_OK)


    #Get all users
    @action(detail=False, methods=['GET'])
    def all(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
    # Custom action for User's Comments
    @action(detail=True, methods=['GET', 'POST'], permission_classes=[IsAuthenticated])
    def comments(self, request, pk=None):
        """
        Retrieve or add comments.
        """
        if request.user.id != int(pk):
            return Response({'detail': 'You can only view or modify your own comments.'}, status=status.HTTP_403_FORBIDDEN)
        
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
        """
        Retrieve or add likes.
        """
        if request.user.id != int(pk):
            return Response({'detail': 'You can only view or modify your own likes.'}, status=status.HTTP_403_FORBIDDEN)
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
        """
        Retrieve or add pets.
        """
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
        """
        Retrieve or add shelters.
        """
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
        
    # Custom action for User's Profile
    @action(detail=True, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def profile(self, request, pk=None):
        """
        Retrieve or update the profile.
        """
        if request.method == 'GET':
            try:
                user = User.objects.get(pk=pk)
            except User.DoesNotExist:
                return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
            
            serializer = UserSerializer(user)
            return Response(serializer.data)
            
        elif request.method == 'PUT':
            # Check if the authenticated user is the same as the user being modified
            if request.user.id != int(pk):
                return Response({'detail': 'You can only modify your own profile.'}, status=status.HTTP_403_FORBIDDEN)
            
            try:
                user = User.objects.get(pk=pk)
            except User.DoesNotExist:
                return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
            
            serializer = UserSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            if request.user.id != int(pk):
                return Response({'detail': 'You can only delete your own profile.'}, status=status.HTTP_403_FORBIDDEN)
            
            user = User.objects.get(pk=pk)
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    def update_user(request, pk):
        user_instance = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user_instance, data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            try:
                serializer.save()
            except ValidationError as e:
                return Response({"username": "A user with that username already exists."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
