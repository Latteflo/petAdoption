from rest_framework import serializers
from .models import Shelter, Pet, Comment, Like, Tag, Pet_Tag, UserProfile
from django.contrib.auth.models import User

class ShelterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shelter
        fields = '__all__'

class PetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = '__all__'
        read_only_fields = ('id', 'date_posted')

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class PetTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet_Tag
        fields = '__all__'
        
class UserLikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'

class UserCommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class UserPetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = '__all__'

class UserSheltersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shelter
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    location = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    likes = UserLikesSerializer(many=True, read_only=True, source='like_set')
    comments = UserCommentsSerializer(many=True, read_only=True, source='comment_set')
    pets = UserPetsSerializer(many=True, read_only=True, source='pet_set')
    shelters = UserSheltersSerializer(many=True, read_only=True, source='shelter_set')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'id', 
                  'location', 'image', 'likes', 'comments', 'pets', 'shelters')
        extra_kwargs = {'password': {'write_only': True}}
        
    def get_location(self, obj):
      profile = UserProfile.objects.filter(user=obj).first()
      return profile.location if profile else "Heaven"

    def get_image(self, obj):
      profile = UserProfile.objects.filter(user=obj).first()
      return profile.image.url if profile and profile.image else "https://cdn-icons-png.flaticon.com/512/1581/1581594.png"