from rest_framework import viewsets, status
from rest_framework.response import Response
from ..models import Comment, Pet, User
from ..serializers import CommentSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

class CommentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for interacting with Comments.
    
    - `list`: Lists comments based on optional pet_pk or user_pk.
    - `retrieve`: Retrieves a specific comment by ID. Restricted to the authenticated user who created the comment.
    - `create`: Creates a new comment. Requires authentication.
    - `update`: Updates a specific comment. Restricted to the authenticated user who created the comment.
    - `destroy`: Deletes a specific comment. Restricted to the authenticated user who created the comment.
    """
    
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        """Assign permissions based on action."""
        if self.action == 'create':
            return [IsAuthenticated()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated()]  
        else:
            return [AllowAny()]
    
    def list(self, request, pet_pk=None, user_pk=None):
      """
      Add pet_pk or user_pk to filter comments by pet or user.
      """
      if pet_pk is not None:
          comments = Comment.objects.filter(pet_id=pet_pk)
      elif user_pk is not None:
          comments = Comment.objects.filter(user_id=user_pk)
      else:
          comments = Comment.objects.all()

      serializer = CommentSerializer(comments, many=True)
      return Response(serializer.data)

    def create(self, request, pet_pk=None):
        """
        Create a new comment. Requires authentication.
        """
        if request.user.is_authenticated:
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid():
                if pet_pk is not None:
                    try:
                        pet_instance = Pet.objects.get(pk=pet_pk)
                    except Pet.DoesNotExist:
                        return Response({'detail': 'Pet not found'}, status=status.HTTP_404_NOT_FOUND)

                    serializer.validated_data['pet'] = pet_instance
                try:
                    user_instance = User.objects.get(username=request.user.username)
                except User.DoesNotExist:
                    return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

                serializer.validated_data['user'] = user_instance

                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED) 
            
    def retrieve(self, request, pk=None):
        """
        Retrieve a specific comment by ID, but only if it belongs to the authenticated user.
        """
        try:
            comment = Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.user.is_authenticated and comment.user == request.user:
            serializer = CommentSerializer(comment)
            return Response(serializer.data)
        else:
            return Response({'detail': 'You do not have permission to view this comment.'}, status=status.HTTP_403_FORBIDDEN)

    def update(self, request, pk=None):
        """
        Update a specific comment. Only the user who created the comment can update it.
        """
        try:
            comment = Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.user.is_authenticated and comment.user == request.user:
            serializer = CommentSerializer(comment, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'detail': 'You do not have permission to update this comment.'}, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, pk=None):
        """
        Delete a specific comment. Only the user who created the comment can delete it.
        """
        try:
            comment = Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.user.is_authenticated and comment.user == request.user:
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'detail': 'You do not have permission to delete this comment.'}, status=status.HTTP_403_FORBIDDEN)
