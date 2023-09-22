from django.contrib import admin
from django.urls import path, include
from pets.views.home import HomeView
from django.conf.urls.static import static
from django.conf import settings  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('', HomeView.as_view(), name='home'),
    path('api/', include('pets.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
