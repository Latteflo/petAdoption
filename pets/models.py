from django.db import models
from django.db import models

class Pet(models.Model):
    name = models.CharField(max_length=100, default='Unknown Name')
    age = models.IntegerField(default=0)
    location = models.CharField(max_length=100, default='Unknown Location')
    personality_traits = models.JSONField(default=dict)
    interests = models.JSONField(default=dict)
    image = models.ImageField(upload_to='images/', default='path/to/default/image.jpg')

    def __str__(self):
        return self.name
    
class Comment(models.Model):
    pet = models.ForeignKey(Pet, related_name='comments', on_delete=models.CASCADE)
    comment = models.TextField(default='No comment')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.pet.name}'
