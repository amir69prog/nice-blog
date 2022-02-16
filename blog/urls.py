from django.urls import path

from .views import PostListView, PostDetailView


app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name='list'),
    path('<str:pk>/', PostDetailView.as_view(), name='detail'),
]