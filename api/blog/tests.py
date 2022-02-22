from datetime import timedelta
import email
from typing import Any, Dict

from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.urls import reverse


from rest_framework.test import APITestCase
from rest_framework import status

from blog.models import Post


User = get_user_model()


class BlogTest(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            phone_number='09211111111',
            username='user1',
            email='useremail1@gmail.com',
            password='123456789',
            is_verified=True
        )
        self.user2 = User.objects.create_user(
            phone_number='09222222222',
            username='user2',
            email='useremail2@gmail.com',
            password='123456789',
            is_verified=True
        )
        self.post1 = Post.objects.create(
            author=self.user1,
            title='Post one title',
            body='Post one body',
            reading_time=timedelta(seconds=300) # 5min
        )


    def authenticate(self, phone_number: str, password: str) -> str:
        """ Get the access key then authenticate with the token """
        url = reverse('token_obtain_pair')  # url getting token
        response = self.client.post(
            url,
            {
                'phone_number': phone_number,
                'password': password
            },
        )
        access_key = response.json().get('access')
        return 'Bearer ' + access_key

    def test_blog_list_view(self):
        access_key = self.authenticate('09211111111', '123456789')
        url = reverse('api-blog:list')
        response = self.client.get(url, HTTP_AUTHORIZATION=access_key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_post(self):
        payload = {
            "title": "Post two title",
            "body": "Post two body",
            "reading_time": '300'
        }

        access_key = self.authenticate('09211111111', '123456789')
        url = reverse('api-blog:list')
        response = self.client.post(url, data=payload, HTTP_AUTHORIZATION=access_key)
        post2 = Post.objects.filter(id=2).get()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 2)
        self.assertEqual(post2.author, self.user1)
        self.assertEqual(post2.title, 'Post two title')
        self.assertEqual(post2.body, 'Post two body')
        self.assertEqual(post2.reading_time, timedelta(seconds=300))
    
    def test_update_post(self):
        payload = {
            "title": "Post two title",
            "body": "Post two body",
            "reading_time": '300'
        }

        access_key = self.authenticate('09211111111', '123456789')
        url = reverse('api-blog:list')
        response = self.client.post(url, data=payload, HTTP_AUTHORIZATION=access_key)
        post2 = Post.objects.filter(id=2).get()

        payload_update = {
            "title": "Post two title updated",
            "body": "Post two body updated",
            "reading_time": '600'
        }

        post2 = Post.objects.filter(id=post2.id).get()
        url = reverse('api-blog:detail', args=(post2.id,))
        response = self.client.put(url, data=payload_update, HTTP_AUTHORIZATION=access_key)
        post2 = Post.objects.filter(id=post2.id).get() # call again becouse it was cached

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(post2.author, self.user1)
        self.assertEqual(post2.title, 'Post two title updated')
        self.assertEqual(post2.body, 'Post two body updated')
        self.assertEqual(post2.reading_time, timedelta(seconds=600))
    
    def test_delete_post(self):
        payload = {
            "title": "Post two title",
            "body": "Post two body",
            "reading_time": '300'
        }

        access_key = self.authenticate('09211111111', '123456789')
        url = reverse('api-blog:list')
        response = self.client.post(url, data=payload, HTTP_AUTHORIZATION=access_key)
        post2 = Post.objects.get(id=2)
        url_del = reverse('api-blog:detail', args=(post2.id,))
        response = self.client.delete(url_del, HTTP_AUTHORIZATION=access_key)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_update_or_delete_not_own_post(self):
        access_key = self.authenticate('09222222222', '123456789')
        
        payload_update = {
            "title": "Post two title updated",
            "body": "Post two body updated",
            "reading_time": '600'
        }

        url = reverse('api-blog:detail', args=(self.post1.id,))
        response = self.client.put(url, data=payload_update, HTTP_AUTHORIZATION=access_key)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
        response = self.client.delete(url, HTTP_AUTHORIZATION=access_key)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
