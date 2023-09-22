from rest_framework_nested import routers
from django.urls import path, include
#from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from pets.views.user_viewset import  UserViewSet
from pets.views.shelter_viewset import ShelterViewSet
from pets.views.pet_viewset import PetViewSet
from pets.views.comment_viewset import CommentViewSet
from pets.views.tag_viewset import TagViewSet
from pets.views.pet_tag_viewset import PetTagViewSet
from pets.views.like_viewset import LikeViewSet

router = routers.DefaultRouter()

# Main routes
router.register(r'pets', PetViewSet, basename='pet')
router.register(r'shelters', ShelterViewSet, basename='shelter')
router.register(r'users', UserViewSet, basename='user')


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
    # JWT token routes
    #path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    #path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Existing routes
    path('', include(router.urls)),
    path('', include(pets_router.urls)),
    path('', include(shelters_router.urls)),
]