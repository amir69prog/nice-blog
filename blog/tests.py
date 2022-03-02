from datetime import timedelta

from django.test import TestCase
from django.urls import reverse, resolve

from blog.views import PostDetailView, PostListView
from accounts.views import user_profile_view
from .models import Post, User


class BlogTests(TestCase):
    
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            phone_number='09121212121',
            username='testuser',
            email='testuser@gmail.com',
            password='123456789',
            is_verified=True
        )
        
        self.user2 = User.objects.create_user(
            phone_number='09111111111',
            username='testuser2',
            email='testuser2@gmail.com',
            password='123456789',
            is_verified=True
        )

        self.post = Post.objects.create(
            author=self.user,
            subheading='Subheading',
            title='Title',
            body='Body',
            reading_time=timedelta(seconds=300)
        )

        self.post2 = Post.objects.create(
            author=self.user2,
            subheading='Subheading',
            title='Title',
            body='Body',
            reading_time=timedelta(seconds=300)
        )
    
    def login(self):
        self.client.login(phone_number='09121212121', password='123456789')

    def test_post_content(self):
        self.assertEqual(self.post.author.phone_number, '09121212121')
        self.assertEqual(self.post.subheading, 'Subheading')
        self.assertEqual(self.post.title, 'Title')
        self.assertEqual(self.post.body, 'Body')
        self.assertEqual(self.post.reading_time, timedelta(seconds=300))
    
    def test_post_list_view(self):
        self.login()

        url = reverse('blog:list')
        view = resolve(url)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Subheading')
        self.assertTemplateUsed(response, 'blog/index.html')
        self.assertEqual(view.func.__name__, PostListView.as_view().__name__)
    
    def test_post_detail_view(self):
        self.login()

        url = reverse('blog:detail', kwargs={'pk': self.post.id, 'slug': self.post.slug})
        view = resolve(url)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Title')
        self.assertContains(response, 'Subheading')
        self.assertTemplateUsed(response, 'blog/post.html')
        self.assertEqual(view.func.__name__, PostDetailView.as_view().__name__)
    
    def test_create_post(self):

        url = reverse('blog:add')
        payload = {
            'title': 'Title 2',
            'subheading': 'Subheading 2',
            'body': 'Body 2',
            'reading_time': timedelta(seconds=500)
        }
        self.login()
        response = self.client.post(url, data=payload, follow=True)
        post = Post.objects.get(id=3)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Post.objects.count(), 3)
        self.assertEqual(post.title, payload['title'])
        self.assertEqual(post.subheading, payload['subheading'])
        self.assertEqual(post.body, payload['body'])
        self.assertEqual(post.reading_time, payload['reading_time'])

    def test_update_post(self):
        # Creating post
        url = reverse('blog:add')
        payload = {
            'title': 'Title 2',
            'subheading': 'Subheading 2',
            'body': 'Body 2',
            'reading_time': timedelta(seconds=500)
        }
        self.login()
        response = self.client.post(url, data=payload, follow=True)
        post = Post.objects.get(id=3)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Post.objects.count(), 3)
        self.assertEqual(post.title, payload['title'])
        self.assertEqual(post.subheading, payload['subheading'])
        self.assertEqual(post.body, payload['body'])
        self.assertEqual(post.reading_time, payload['reading_time'])

        # Updating the created post
        update_url = reverse('blog:edit', kwargs={'pk': post.id, 'slug':post.slug})
        update_payload = {
            'title': 'Title 2 Updated',
            'subheading': 'Subheading 2 Updated',
            'body': 'Body 2 Updated',
            'reading_time': timedelta(seconds=600)
        }
        response = self.client.post(update_url, data=update_payload, follow=True)
        post = Post.objects.get(id=3)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(post.title, update_payload['title'])
        self.assertEqual(post.subheading, update_payload['subheading'])
        self.assertEqual(post.body, update_payload['body'])
        self.assertEqual(post.reading_time, update_payload['reading_time'])
    
    def test_delete_post(self):
        # Creating post
        url = reverse('blog:add')
        payload = {
            'title': 'Title 2',
            'subheading': 'Subheading 2',
            'body': 'Body 2',
            'reading_time': timedelta(seconds=500)
        }
        self.login()
        response = self.client.post(url, data=payload, follow=True)
        post = Post.objects.get(id=3)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Post.objects.count(), 3)
        self.assertEqual(post.title, payload['title'])
        self.assertEqual(post.subheading, payload['subheading'])
        self.assertEqual(post.body, payload['body'])
        self.assertEqual(post.reading_time, payload['reading_time'])

        # Deleting the created post
        delete_url = reverse('blog:delete', kwargs={'pk': post.id, 'slug':post.slug})
        
        response = self.client.delete(delete_url, follow=True)
        self.assertEqual(Post.objects.count(), 2)
        self.assertEqual(response.status_code, 200)
    
    def test_delete_not_own_post(self):
        # Deleting the post 2 that is not for logged in user
        self.login()
        delete_url = reverse('blog:delete', kwargs={'pk': self.post2.id, 'slug':self.post2.slug})
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'You haven\'t access to view this page')
    
    def test_update_not_own_post(self):
        update_url = reverse('blog:edit', kwargs={'pk': self.post2.id, 'slug':self.post2.slug})
        update_payload = {
            'title': 'Title 2 Updated',
            'subheading': 'Subheading 2 Updated',
            'body': 'Body 2 Updated',
            'reading_time': timedelta(seconds=600)
        }
        self.login()
        response = self.client.post(update_url, data=update_payload, follow=True)
        post = Post.objects.get(id=2)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'You haven\'t access to view this page')
        self.assertNotEqual(post.title, update_payload['title'])
        self.assertNotEqual(post.subheading, update_payload['subheading'])
        self.assertNotEqual(post.body, update_payload['body'])
        self.assertNotEqual(post.reading_time, update_payload['reading_time'])