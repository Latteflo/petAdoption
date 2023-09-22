from rest_framework import viewsets, status
from rest_framework.response import Response
from ..models import Like
from ..serializers import LikeSerializer
from rest_framework.decorators import authentication_classes
from rest_framework.authentication import SessionAuthentication

@authentication_classes([SessionAuthentication])
class LikeViewSet(viewsets.ModelViewSet):
    
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    
    def list(self, request):
        likes = Like.objects.all()
        serializer = LikeSerializer(likes, many=True)
        return Response(serializer.data)
        
    def create(self, request):
        if request.user.is_authenticated:
            serializer = LikeSerializer(data=request.data)
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
        serializer = LikeSerializer(like)
        return Response(serializer.data)
        
    def update(self, request, pk=None):
        try:
            like = Like.objects.get(pk=pk)
        except Like.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        if request.user.is_authenticated:
            serializer = LikeSerializer(like, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)
        
    def destroy(self, request, pk=None):
        try:
            like = Like.objects.get(pk=pk)
        except Like.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        if request.user.is_authenticated:
            like.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)
