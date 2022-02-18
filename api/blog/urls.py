from django.urls import path

from .views import PostListAPIView, PostDetailAPIView

app_name = 'api-blog'

urlpatterns = [
    path('', PostListAPIView.as_view(), name='list'),
    path('<str:pk>/', PostDetailAPIView.as_view(), name='detail'),
]