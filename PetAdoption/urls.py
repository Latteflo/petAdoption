from django.contrib import admin
from django.urls import path, include
from pets.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('pets.urls')),
    path('', home, name='home'),
]
