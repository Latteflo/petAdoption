from rest_framework_nested import routers
from django.urls import path, include
from pets.views.shelter_viewset import ShelterViewSet
from pets.views.pet_viewset import PetViewSet
from pets.views.comment_viewset import CommentViewSet
from pets.views.tag_viewset import TagViewSet
from pets.views.pet_tag_viewset import PetTagViewSet
from pets.views.like_viewset import LikeViewSet
from pets.views.user_viewset import UserViewSet
from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view

router = routers.DefaultRouter()

# Main routes
router.register(r'pets', PetViewSet, basename='pet')
router.register(r'shelters', ShelterViewSet, basename='shelter')
router.register(r'users', UserViewSet, basename='user')
router.register(r'tags', TagViewSet, basename='tags')
router.register(r'pet_tags', PetTagViewSet, basename='pet_tag')

# Nested routes for users
users_router = routers.NestedSimpleRouter(router, r'users', lookup='user')
users_router.register(r'comments', CommentViewSet, basename='comment')
users_router.register(r'likes', LikeViewSet, basename='like')
users_router.register(r'pets', PetViewSet, basename='pet')

# Nested routes for pets
pets_router = routers.NestedSimpleRouter(router, r'pets', lookup='pet')
pets_router.register(r'comments', CommentViewSet, basename='comment')
pets_router.register(r'likes', LikeViewSet, basename='like')
pets_router.register(r'tags', TagViewSet, basename='tag')
pets_router.register(r'pet_tags', PetTagViewSet, basename='pet_tag')

# Nested routes for shelters
shelters_router = routers.NestedSimpleRouter(router, r'shelters', lookup='shelter')
shelters_router.register(r'pets', PetViewSet)

urlpatterns = [
# Existing routes
    path('', include(router.urls)),
    path('', include(pets_router.urls)),
    path('', include(shelters_router.urls)),
    path('', include(users_router.urls)),
    path('register/', UserViewSet.as_view({'post': 'register'}), name='user-register'),
    path('login/', UserViewSet.as_view({'post': 'login'}), name='user-login'),
    path('docs/', include_docs_urls(title='PetAdoption API', description='Welcome to the PetAdoption API documentation. This API is designed to facilitate the development of a pet adoption platform that seeks to provide an efficient, streamlined process for connecting prospective pet owners with animal shelters. Our backend is built using a robust stack including PostgreSQL, Python, and Django REST Framework, aiming for high scalability, data integrity, and easy maintainability.')),
    path('schema/', get_schema_view(
        title='PetAdoption API',
        description='API for all things related to pet adoption',
        version='1.0.0'
    ), name='openapi-schema'),
]