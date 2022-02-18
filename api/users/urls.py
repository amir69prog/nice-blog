from django.urls import path

from .views import UserListAPIView, UserDetailAPIView

app_name = 'api-user'

urlpatterns = [
    path('', UserListAPIView.as_view(), name='list'),
    path('<str:pk>/', UserDetailAPIView.as_view(), name='detail'),
]