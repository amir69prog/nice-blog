from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    
    # API VERSION 1
    path('api/v1/blog/', include('api.blog.urls')),
    path('api/v1/users/', include('api.users.urls')),
    
    # AUTHENTICATION
    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/dj-rest-auth/', include('dj_rest_auth.urls')),
    path('api/v1/dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
]
