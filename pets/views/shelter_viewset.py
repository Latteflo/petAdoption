from rest_framework import viewsets, status
from rest_framework.decorators import action, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..models import Shelter, Comment, Like, Pet, Tag
from ..serializers import ShelterSerializer, CommentSerializer, LikeSerializer, PetSerializer, TagSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication


@authentication_classes([JWTAuthentication])
class ShelterViewSet(viewsets.ModelViewSet):
    
    queryset = Shelter.objects.all()
    serializer_class = ShelterSerializer
    
    def list(self, request):
        shelters = Shelter.objects.all()
        serializer = ShelterSerializer(shelters, many=True)
        return Response(serializer.data)
        
    def create(self, request):
        if request.user.is_authenticated:
            serializer = ShelterSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)
            
    def retrieve(self, request, pk=None):
        try:
            shelter = Shelter.objects.get(pk=pk)
        except Shelter.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ShelterSerializer(shelter)
        return Response(serializer.data)
        
    def update(self, request, pk=None):
        try:
            shelter = Shelter.objects.get(pk=pk)
        except Shelter.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        if request.user.is_authenticated:
            serializer = ShelterSerializer(shelter, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)
        
    def destroy(self, request, pk=None):
        try:
            shelter = Shelter.objects.get(pk=pk)
        except Shelter.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        if request.user.is_authenticated:
            shelter.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)

    # Custom action for Shelter's Pets
    @action(detail=True, methods=['GET', 'POST'], permission_classes=[IsAuthenticated])
    def pets(self, request, pk=None):
        if request.method == 'GET':
            pets = Pet.objects.filter(shelter=pk)
            serializer = PetSerializer(pets, many=True)
            return Response(serializer.data)
        elif request.method == 'POST':
            serializer = PetSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(shelter_id=pk)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Custom action for Shelter's Comments
    @action(detail=True, methods=['GET', 'POST'], permission_classes=[IsAuthenticated])
    def comments(self, request, pk=None):
        if request.method == 'GET':
            comments = Comment.objects.filter(shelter=pk)
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data)
        elif request.method == 'POST':
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(shelter_id=pk)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Custom action for Shelter's Likes
    @action(detail=True, methods=['GET', 'POST'], permission_classes=[IsAuthenticated])
    def likes(self, request, pk=None):
        if request.method == 'GET':
            likes = Like.objects.filter(shelter=pk)
            serializer = LikeSerializer(likes, many=True)
            return Response(serializer.data)
        elif request.method == 'POST':
            serializer = LikeSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(shelter_id=pk)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Custom action for Shelter's Tags
    @action(detail=True, methods=['GET', 'POST'], permission_classes=[IsAuthenticated])
    def tags(self, request, pk=None):
        if request.method == 'GET':
            tags = Tag.objects.filter(shelter=pk)
            serializer = TagSerializer(tags, many=True)
            return Response(serializer.data)
        elif request.method == 'POST':
            serializer = TagSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(shelter_id=pk)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)