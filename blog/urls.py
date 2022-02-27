from django.urls import path

from .views import PostListView, PostDetailView, CreatePostView, DeletePostView, UpdatePostView


app_name = 'blog'
urlpatterns = [
    path('', PostListView.as_view(), name='list'),
    path('<int:pk>/<str:slug>/', PostDetailView.as_view(), name='detail'),
    path('add/', CreatePostView.as_view(), name='add'),
    path('<int:pk>/<str:slug>/delete/', DeletePostView.as_view(), name='delete'),
    path('<int:pk>/<str:slug>/edit/', UpdatePostView.as_view(), name='edit'),
]