from rest_framework import viewsets, status
from rest_framework.response import Response
from ..models import Tag, Pet_Tag
from ..serializers import TagSerializer
from rest_framework.permissions import IsAuthenticated , AllowAny , IsAdminUser

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        elif self.action in ['destroy']:
            return [IsAdminUser()]
        else:
            return [AllowAny()]
    
    def list(self, request, pet_pk=None):
        if pet_pk is not None:
            pet_tags = Pet_Tag.objects.filter(pet_id=pet_pk)
            tags = [pt.tag for pt in pet_tags]
        else:
            tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)

    def create(self, request, pet_pk=None):
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
        try:
            tag = Tag.objects.get(pk=pk)
        except Tag.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = TagSerializer(tag)
        return Response(serializer.data)

    def update(self, request, pk=None, pet_pk=None):
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
        try:
            tag = Tag.objects.get(pk=pk)
        except Tag.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        if request.user.is_authenticated:
            tag.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)
