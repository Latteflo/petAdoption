from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='user_images/')
    location = models.CharField(max_length=100)
    
    class Meta:
        ordering = ['user__username']
    
    def __str__(self):
        return self.user.username
    
# Shelter Information Table      
class Shelter(models.Model):
    img = models.CharField(max_length=255, null=True, blank=True, default='default_shelter.jpg')
    name = models.CharField(max_length=200, default='Shelter Angels on Earth')
    location = models.CharField(max_length=200, default='Heaven')
    description = models.TextField(default='A place for animals to live.')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, related_name='shelters', default='1')
    
    class Meta:
        ordering = ['name'] 
        
    def __str__(self):
        return self.name
    
 # Pet Information Table
class Pet(models.Model):
    img = models.CharField(max_length=255, null=True, blank=True, default='default_pet.jpg')
    name = models.CharField(max_length=100, default='Fluffy McFluffFace')
    pet_type = models.CharField(max_length=100, default='Mystery Animal')
    characteristics = models.TextField(null=True, blank=True, default='Adorable and mysterious')
    age = models.IntegerField(null=True, blank=True, default=0, help_text='Age in months')
    @property
    def age_in_years(self):
        return self.age // 12  
    gender = models.CharField(max_length=50, null=True, blank=True, default='Unknown')
    description = models.TextField(default='A pet shrouded in adorable mystery.')
    status = models.CharField(max_length=100, default='Looking for belly rubs')
    location = models.CharField(max_length=255, null=True, blank=True, default='Couch')
    shelter = models.ForeignKey(Shelter, related_name='pets', on_delete=models.CASCADE, null=True, blank=True)
    date_posted = models.DateField(auto_now_add=True, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    tags = models.ManyToManyField('Tag', through='Pet_Tag', related_name='pets')
    
    class Meta:
        ordering = ['id'] 
        
    def __str__(self):
        return self.name

# Comments on Pet Table
class Comment(models.Model):
    text = models.TextField(default='So cute!')
    date_commented = models.DateTimeField(default=timezone.now)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, default='3')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    
    class Meta:
        ordering = ['date_commented'] 
        
    def __str__(self):
        return self.text
    
    

# Likes on Posts Table
class Like(models.Model):
    date_liked = models.DateField(auto_now_add=True)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, default='3')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, related_name='likes')
    

# Tags for Pet Personality Traits Table
class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True, default='Cute')
    
    def __str__(self):
        return self.name

# Junction Table for Pet and Tags
class Pet_Tag(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
