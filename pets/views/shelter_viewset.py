from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from ..models import Shelter, Comment, Like, Pet
from ..serializers import ShelterSerializer, CommentSerializer, LikeSerializer, PetSerializer

class ShelterViewSet(viewsets.ModelViewSet):
    """
    API endpoint for interacting with Shelters.
    
    - `list`: Lists all shelters. No authentication required.
    - `retrieve`: Retrieves a specific shelter by ID. No authentication required.
    - `create`: Creates a new shelter. Requires authentication.
    - `update`, `partial_update`, `destroy`: Modifies or deletes a shelter. Requires admin privileges.
    
    Additional actions:
    - `pets`: List or add pets for a specific shelter.
    - `comments`: List or add comments for a specific shelter.
    - `likes`: List or add likes for a specific shelter.
    """
    
    queryset = Shelter.objects.all()
    serializer_class = ShelterSerializer

    def get_permissions(self):
        """Assign permissions based on action."""
        if self.action == 'create':
            return [IsAuthenticated()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        else:
            return [AllowAny()]

    def list(self, request):
        """List all shelters."""
        shelters = Shelter.objects.all()
        serializer = ShelterSerializer(shelters, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Create a new shelter. Requires authentication."""
        if request.user.is_authenticated:
            serializer = ShelterSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(owner=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)
  
    def retrieve(self, request, pk=None):
        """
        Retrieve a specific shelter by ID.
        """
        try:
            shelter = Shelter.objects.get(pk=pk)
        except Shelter.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ShelterSerializer(shelter)
        return Response(serializer.data)
        
    def update(self, request, pk=None):
        """
        Update a shelter's information.
        """
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
        """
        Delete a shelter.
        """
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
        """
        List or add pets for a specific shelter.
        """
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
        """
        List or add comments for a specific shelter.
        """
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
        """
        List or add likes for a specific shelter.
        """
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
