from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from ..models import Comment, Like, Pet, Shelter
from ..serializers import UserSerializer, CommentSerializer, LikeSerializer, PetSerializer, ShelterSerializer
from django.contrib.auth import authenticate, get_user_model
from rest_framework.authtoken.models import Token
    
class UserViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    # Custom action for User's Registration
    @action(detail=False, methods=['POST'], url_path='register')
    def register(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            email = serializer.validated_data['email']
         
            if User.objects.filter(username=username).exists():
               return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
                
            if User.objects.filter(email=email).exists():
                return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
           
            user = User.objects.create_user(
                username=serializer.validated_data['username'],
                last_name=serializer.validated_data['last_name'],
                first_name=serializer.validated_data['first_name'],
                location=serializer.validated_data['location'],
                password=serializer.validated_data['password'],
                email=serializer.validated_data['email']
            )
            token = Token.objects.create(user=user)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['POST'], url_path='login')
    def login(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        
        user_model = get_user_model()
        
        # If email is provided, try to find the user by email
        if email:
            try:
                user = user_model.objects.get(email=email)
                username = user.username
            except user_model.DoesNotExist:
                return Response({'error': 'Email does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        # If username is provided, try to find the user by username
        if username: 
            try:
                user = user_model.objects.get(username=username)
            except user_model.DoesNotExist:
                return Response({'error': 'Username does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Username not provided'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, email=email, password=password)

        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid username/email or password'}, status=status.HTTP_400_BAD_REQUEST)
    
  # Custom action for User's Comments
    @action(detail=True, methods=['GET', 'POST'], permission_classes=[IsAuthenticated])
    def comments(self, request, pk=None):
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
        
    # Custom action for User's Profile
    @action(detail=True, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def profile(self, request, pk=None):
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
