from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    
    # API VERSION 1
    path('api/v1/blog/', include('api.blog.urls')),
    path('api/v1/users/', include('api.users.urls')),
    
    # AUTHENTICATION
    path('api-auth/', include('rest_framework.urls')),
    
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
