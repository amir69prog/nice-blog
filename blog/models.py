from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.text import slugify

from .messages import PostMessages


User = get_user_model()


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', related_query_name='post')
    title = models.CharField(max_length=200)
    body = models.TextField()
    reading_time = models.DurationField(help_text=PostMessages.READING_TIME_HELP_TEXT.value) # in seconds
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-date_created', '-date_updated')

    def __str__(self) -> str:
        return self.title

    @property
    def slug(self):
        slug = slugify(self.title, allow_unicode=True)
        return slug 

    def get_absolute_url(self):
        slug = self.slug
        return reverse('blog:detail', kwargs={'pk':self.id, 'slug':slug})
