from rest_framework import serializers
from .models import Shelter, Pet, Comment, Like, Tag, Pet_Tag, UserProfile
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    location = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'id', 'user_permissions', 'location', 'image')
        extra_kwargs = {'password': {'write_only': True}}

    def get_location(self, obj):
        profile = UserProfile.objects.get(user=obj)
        return profile.location

    def get_image(self, obj):
        profile = UserProfile.objects.get(user=obj)
        return profile.image.url if profile.image else None

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        UserProfile.objects.update_or_create(user=user, defaults={
            'location': validated_data.get('location', ''),
            'image': validated_data.get('image', '')
        })
        return user

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
