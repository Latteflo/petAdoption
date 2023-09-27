from rest_framework import viewsets, status
from rest_framework.response import Response
from ..models import Tag, Pet_Tag
from ..serializers import TagSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

class TagViewSet(viewsets.ModelViewSet):
    """
    API endpoint for interacting with Tags.
    
    - `list`: Lists all tags. If a pet_pk is provided, lists tags associated with that pet.
    - `retrieve`: Retrieves a specific tag by ID. No authentication required.
    - `create`: Creates a new tag. Requires authentication and a pet_pk.
    - `update`: Updates a specific tag. Requires authentication.
    - `destroy`: Deletes a specific tag. Requires admin privileges.
    """
    
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def get_permissions(self):
        """Assign permissions based on action."""
        if self.action == 'create':
            return [IsAuthenticated()]
        elif self.action == 'destroy':
            return [IsAdminUser()]
        else:
            return [AllowAny()]

    def list(self, request, pet_pk=None):
        """List all tags. If pet_pk is provided, list tags associated with that pet."""
        if pet_pk is not None:
            pet_tags = Pet_Tag.objects.filter(pet_id=pet_pk)
            tags = [pt.tag for pt in pet_tags]
        else:
            tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)

    def create(self, request, pet_pk=None):
        """
        Create a new tag. Requires authentication and a pet_pk.
        """
        if pet_pk is None:
            return Response({'detail': 'Pet ID must be provided.'}, status=status.HTTP_400_BAD_REQUEST)

        if request.user.is_authenticated:
            serializer = TagSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)

    def retrieve(self, request, pk=None):
        """
        Retrieve a specific tag by ID.
        """
        try:
            tag = Tag.objects.get(pk=pk)
        except Tag.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = TagSerializer(tag)
        return Response(serializer.data)

    def update(self, request, pk=None, pet_pk=None):
        """
        Update a specific tag.
        """
        try:
            tag = Tag.objects.get(pk=pk)
        except Tag.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        if request.user.is_authenticated:
            serializer = TagSerializer(tag, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, pk=None):
        """
        Delete a specific tag.
        """
        try:
            tag = Tag.objects.get(pk=pk)
        except Tag.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        if request.user.is_authenticated:
            tag.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)
