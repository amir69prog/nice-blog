from rest_framework import generics, permissions

from blog.models import Post
from api.users.permissions import IsUserVerified

from . import permissions as custom_permission
from .serializers import PostSerializer


class PostListAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by('-date_updated')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsUserVerified]

    def perform_create(self, serializer):
        """ Overwriting this method only for setting the author instance """
        serializer.save(author=self.request.user)


class PostDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated,
                          IsUserVerified, custom_permission.IsAuthorOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
