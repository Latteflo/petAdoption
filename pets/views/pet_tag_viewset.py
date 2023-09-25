from rest_framework import viewsets, status
from rest_framework.response import Response
from ..models import Pet_Tag
from ..serializers import PetTagSerializer
from rest_framework.decorators import authentication_classes
from rest_framework.authentication import SessionAuthentication

@authentication_classes([SessionAuthentication])
class PetTagViewSet(viewsets.ModelViewSet):
    
    queryset = Pet_Tag.objects.all()
    serializer_class = PetTagSerializer
    
    def list(self, request, pet_pk=None, tag_pk=None):
        if pet_pk is not None:
            pet_tags = Pet_Tag.objects.filter(pet_id=pet_pk)
        elif tag_pk is not None:
            pet_tags = Pet_Tag.objects.filter(tag_id=tag_pk)
        else:
            pet_tags = Pet_Tag.objects.all()
            
        serializer = PetTagSerializer(pet_tags, many=True)
        return Response(serializer.data)

    def create(self, request):
        if request.user.is_authenticated:
            serializer = PetTagSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)

    def retrieve(self, request, pk=None):
        try:
            pet_tag = Pet_Tag.objects.get(pk=pk)
        except Pet_Tag.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PetTagSerializer(pet_tag)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            pet_tag = Pet_Tag.objects.get(pk=pk)
        except Pet_Tag.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.user.is_authenticated:
            serializer = PetTagSerializer(pet_tag, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, pk=None):
        try:
            pet_tag = Pet_Tag.objects.get(pk=pk)
        except Pet_Tag.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.user.is_authenticated:
            pet_tag.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)
