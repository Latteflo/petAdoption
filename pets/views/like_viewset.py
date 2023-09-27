from rest_framework import viewsets, status
from rest_framework.response import Response
from ..models import Like
from ..serializers import LikeSerializer
from rest_framework.permissions import IsAuthenticated , AllowAny, IsAdminUser


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        else:
            return [AllowAny()]
    
    
    def list(self, request, pet_pk=None, user_pk=None):
        if request.user.is_authenticated:
            if pet_pk is not None:
                likes = Like.objects.filter(pet_id=pet_pk, user=request.user)
            elif user_pk is not None and str(user_pk) == str(request.user.id):
                likes = Like.objects.filter(user_id=user_pk)
            else:
                likes = Like.objects.filter(user=request.user)
        else:
            return Response({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = LikeSerializer(likes, many=True)
        return Response(serializer.data)

    def create(self, request, pet_pk=None, user_pk=None):
        if request.user.is_authenticated:
            data = request.data.copy()
            data['user'] = request.user.id
            if pet_pk is not None:
                data['pet'] = pet_pk
            elif user_pk is not None:
                data['user'] = user_pk

            serializer = LikeSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)

    def retrieve(self, request, pk=None):
        try:
            like = Like.objects.get(pk=pk)
        except Like.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.user.is_authenticated and like.user == request.user:
            serializer = LikeSerializer(like)
            return Response(serializer.data)
        else:
            return Response({'detail': 'You do not have permission to view this like.'}, status=status.HTTP_403_FORBIDDEN)

    def update(self, request, pk=None):
        try:
            like = Like.objects.get(pk=pk)
        except Like.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.user.is_authenticated and like.user == request.user:
            serializer = LikeSerializer(like, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'detail': 'You do not have permission to update this like.'}, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, pk=None):
        try:
            like = Like.objects.get(pk=pk)
        except Like.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.user.is_authenticated and like.user == request.user:
            like.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'detail': 'You do not have permission to delete this like.'}, status=status.HTTP_403_FORBIDDEN)
