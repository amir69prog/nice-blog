from datetime import timedelta
from urllib import response

from django.test import TestCase
from django.urls import reverse, resolve

from blog.views import PostDetailView, PostListView

from .models import Post, User


class BlogTests(TestCase):
    
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@gmail.com'
        )

        self.post = Post.objects.create(
            author=self.user,
            title='Some good title',
            body='Some good body',
            reading_time=timedelta(seconds=300)
        )
    
    def test_post_cotent(self):
        self.assertEqual(self.post.author.username, self.user.username)
        self.assertEqual(self.post.title, 'Some good title')
        self.assertEqual(self.post.body, 'Some good body')
        self.assertEqual(self.post.reading_time.seconds, 300)
    
    def test_post_list_view(self):
        url = reverse('blog:list')
        view = resolve(url)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_list.html')
        self.assertContains(response, 'Some good title')
        self.assertContains(response, 'Read more')
        self.assertEqual(view.func.__name__, PostListView.as_view().__name__)

    def test_post_detail_view(self):
        url = reverse('blog:detail', args=(1,))
        view = resolve(url)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_detail.html')
        self.assertContains(response, 'Some good title')
        self.assertEqual(view.func.__name__, PostDetailView.as_view().__name__)

    def test_wrong_post_detail_view(self):
        url = reverse('blog:detail', args=(2,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)



        