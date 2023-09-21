from django.db import models

class Pet(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    location = models.CharField(max_length=100)
    personality_traits = models.JSONField()
    interests = models.JSONField()
    image = models.ImageField(upload_to='pets/')

    def __str__(self):
        return self.name
    
class Comment(models.Model):
    pet = models.ForeignKey(Pet, related_name='comments', on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.pet.name}'
