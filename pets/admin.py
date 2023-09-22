from django.contrib import admin
from django.contrib.auth.models import User
from .models import Shelter, Pet, Comment, Like, Tag, Pet_Tag

# Register your models here.
admin.site.unregister(User)
admin.site.register(Shelter)
admin.site.register(Pet)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Tag)
admin.site.register(Pet_Tag)
