from rest_framework import viewsets, status
from rest_framework.response import Response
from ..models import Pet
from ..serializers import PetSerializer
from rest_framework.decorators import authentication_classes, action
from rest_framework.authentication import SessionAuthentication

@authentication_classes([SessionAuthentication])
class PetViewSet(viewsets.ModelViewSet):
    
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    filterset_fields = ['shelter']

    def list(self, request):
        pets = Pet.objects.all()
        serializer = PetSerializer(pets, many=True)
        return Response(serializer.data)
        
    def create(self, request):
        if request.user.is_authenticated:
            serializer = PetSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)
            
    def retrieve(self, request, pk=None):
        try:
            pet = Pet.objects.get(pk=pk)
        except Pet.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PetSerializer(pet)
        return Response(serializer.data)
        
    def update(self, request, pk=None):
        try:
            pet = Pet.objects.get(pk=pk)
        except Pet.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        if request.user.is_authenticated:
            serializer = PetSerializer(pet, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)
        
    def destroy(self, request, pk=None):
        try:
            pet = Pet.objects.get(pk=pk)
        except Pet.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        if request.user.is_authenticated:
            pet.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)
    
    def get_queryset(self):
       queryset = Pet.objects.all()
    
       # Filtering by shelter
       shelter_id = self.request.query_params.get('shelter', None)
       if shelter_id is not None:
          queryset = queryset.filter(shelter=shelter_id)
        
       # Filtering by tags
       tag_id = self.request.query_params.get('tag', None)
       if tag_id is not None:
          queryset = queryset.filter(tags__id=tag_id)
        
       # Filtering by likes
       like_id = self.request.query_params.get('like', None)
       if like_id is not None:
          queryset = queryset.filter(likes__id=like_id)
        
      # Filtering by user (creator)
       user_id = self.request.query_params.get('user', None)
       if user_id is not None:
          queryset = queryset.filter(user=user_id)

       return queryset

    
