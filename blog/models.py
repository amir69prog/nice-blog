from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse


User = get_user_model()

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', related_query_name='post')
    title = models.CharField(max_length=200)
    body = models.TextField()
    reading_time = models.DurationField(blank=True) # in seconds
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog:detail', args=(self.id,))
