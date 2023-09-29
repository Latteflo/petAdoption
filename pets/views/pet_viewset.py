from rest_framework import viewsets, status
from rest_framework.response import Response
from ..models import Pet, Tag
from ..serializers import PetSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework import filters 

class PetViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing pets.

    This view provides the following functionalities:
    - List all pets: GET /pets/
    - Create a new pet: POST /pets/
    - Retrieve a pet by ID: GET /pets/{id}/
    - Update a pet by ID: PUT /pets/{id}/
    - Partially update a pet by ID: PATCH /pets/{id}/
    - Delete a pet by ID: DELETE /pets/{id}/

    Query Parameters:
    - `shelter`: Filter pets by shelter ID
    - `tags`: Filter pets by tags
    - `likes`: Filter pets by likes
    - `user`: Filter pets by user (creator)

    Permission Levels:
    - Any user can list and retrieve pets.
    - Only authenticated users can create pets.
    - Only admin users can update or delete pets.
    """
    queryset = Pet.objects.all()
    serializer_class = PetSerializer   
    filter_backends = (filters.BaseFilterBackend,)
    filterset_fields = ['shelter', 'tags', 'likes', 'user', 'gender']

    def get_permissions(self):
        """
        Determine the permissions that the user has.
        """ 
        
        if self.action == 'create':
            return [IsAuthenticated()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        else:
            return [AllowAny()]

    def list(self, request):
        """
        List all pets in the database.
        """
        pets = Pet.objects.all()
        serializer = PetSerializer(pets, many=True)
        return Response(serializer.data)
        
    def create(self, request):
        """
        Create a new pet.
        
        Required Fields:
        - name: string
        - age: integer
        - breed: string
        - shelter: Shelter object ID
        - (Optional) tags: list of tag names
        """
        if request.user.is_authenticated:
            serializer = PetSerializer(data=request.data)
            if serializer.is_valid():
                # Save the pet instance and get it back
                pet = serializer.save()
                
                # Add tags (received as list of tag names)
                tag_names = request.data.get('tags', [])
                tags = Tag.objects.filter(name__in=tag_names)
                for tag in tags:
                    pet.tags.add(tag)
                
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)


    def retrieve(self, request, pk=None):
        """
        Retrieve a single pet by its ID.
        """
        try:
            pet = Pet.objects.get(pk=pk)
        except Pet.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PetSerializer(pet)
        return Response(serializer.data)
        
    def update(self, request, pk=None):
        """
        Update an existing pet by its ID.
        """
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
        """
        Delete a pet by its ID.
        """
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
       """
       Get the list of pets for the current user based on the provided query parameters.
       """
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
          
      # Filtering by Gender
       gender = self.request.query_params.get('gender', None)
       if gender is not None:
           queryset = queryset.filter(gender=gender)
            
       return queryset

    
