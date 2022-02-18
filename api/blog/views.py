from rest_framework import generics, permissions

from . import permissions as custom_permission
from .serializers import PostSerializer
from blog.models import Post


class PostListAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by('-date_updated')
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        """ Overwriting this method only for setting the author instance """
        serializer.save(author=self.request.user)


class PostDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, custom_permission.IsAuthorOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
