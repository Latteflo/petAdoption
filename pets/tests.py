#from django.test import TestCase
#from django.urls import reverse
#from rest_framework.test import APIClient, APITestCase
#from rest_framework import status
#from django.contrib.auth.models import User
#from .models import Shelter, Pet, Comment, Like, Tag, Pet_Tag

## Model Tests
#class ShelterModelTestCase(TestCase):
#    def setUp(self):
#        self.user = User.objects.create_user(username='testuser', password='testpass')
#        self.shelter = Shelter.objects.create(
#            name="Animal Haven",
#            location="New York",
#            description="A shelter for homeless animals.",
#            user_id=self.user
#        )

#    def test_shelter_creation(self):
#        self.assertIsInstance(self.shelter, Shelter)
#        self.assertEqual(self.shelter.__str__(), self.shelter.name)

#class PetModelTestCase(TestCase):
#    def setUp(self):
#        self.user = User.objects.create_user(username='testuser', password='testpass')
#        self.shelter = Shelter.objects.create(
#            name="Animal Haven",
#            location="New York",
#            description="A shelter for homeless animals.",
#            user_id=self.user
#        )
#        self.pet = Pet.objects.create(
#            name="Buddy",
#            pet_type="Dog",
#            age=3,
#            gender="Male",
#            shelter=self.shelter,
#            user_id=self.user
#        )

#    def test_pet_creation(self):
#        self.assertIsInstance(self.pet, Pet)
#        self.assertEqual(self.pet.__str__(), self.pet.name)
        
#class CommentModelTestCase(TestCase):
#    def setUp(self):
#        self.user = User.objects.create_user(username='testuser', password='testpass')
#        self.pet = Pet.objects.create(name="Fluffy", pet_type="Cat", user_id=self.user.id)
#        self.comment = Comment.objects.create(text="So adorable!", pet=self.pet, user_id=self.user)

#    def test_comment_creation(self):
#        self.assertIsInstance(self.comment, Comment)
#        self.assertEqual(self.comment.__str__(), self.comment.text)
        
#class LikeModelTestCase(TestCase):
#    def setUp(self):
#        self.user = User.objects.create_user(username='testuser', password='testpass')
#        self.pet = Pet.objects.create(name="Fluffy", pet_type="Cat", user_id=self.user)
#        self.like = Like.objects.create(pet=self.pet, user_id=self.user)

#    def test_like_creation(self):
#        self.assertIsInstance(self.like, Like)


#class TagModelTestCase(TestCase):
#    def setUp(self):
#        self.tag = Tag.objects.create(name="Friendly")

#    def test_tag_creation(self):
#        self.assertIsInstance(self.tag, Tag)
#        self.assertEqual(self.tag.__str__(), self.tag.name)


#class PetTagModelTestCase(TestCase):
#    def setUp(self):
#        self.user = User.objects.create_user(username='testuser', password='testpass')
#        self.pet = Pet.objects.create(name="Fluffy", pet_type="Cat", user_id=self.user)
#        self.tag = Tag.objects.create(name="Friendly")
#        self.pet_tag = Pet_Tag.objects.create(pet=self.pet, tag=self.tag)

#    def test_pet_tag_creation(self):
#        self.assertIsInstance(self.pet_tag, Pet_Tag)
