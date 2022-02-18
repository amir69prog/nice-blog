from rest_framework import generics, permissions

from . import permissions as custom_permission
from .serializers import UserSerializer
from blog.models import User


class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, custom_permission.IsSelfOrReadOnly]
    queryset = User.objects.all()
    serializer_class = UserSerializer

