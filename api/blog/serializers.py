from rest_framework import serializers

from blog.models import Post


class PostSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Post
        fields = ('id', 'title', 'subheading', 'author', 'body', 'reading_time', 'date_created', 'date_updated')
        read_only_fields = ['author',]