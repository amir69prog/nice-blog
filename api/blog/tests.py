from datetime import timedelta
from typing import Any, Dict

from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.urls import reverse


from rest_framework.test import APITestCase
from rest_framework import status

from blog.models import Post


User = get_user_model()


class BlogAPITests(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1', password='passuser1')
        self.user2 = User.objects.create_user(
            username='user2', password='passuser2')
        self.post1 = Post.objects.create(
            author=self.user1,
            title='title',
            body='body',
            reading_time=timedelta(seconds=300)
        )

    def login_by_session(test_func, username='user1', password='passuser1'):
        def wrapper(self):
            self.client.login(username=username, password=password)
            return test_func(self)
        return wrapper

    def get_response_post_list_view(self) -> HttpResponse:
        """ Return response for PostListView """
        url = reverse('api-blog:list')
        response = self.client.get(url)
        return response

    def get_response_post_detail_view(self, id: int) -> HttpResponse:
        """ Return response for PostDetailView """
        url = reverse('api-blog:detail', kwargs={'pk': id})
        response = self.client.get(url)
        return response

    def create_post(self, payload: Dict, header: Dict) -> HttpResponse:
        url = reverse('api-blog:list')
        response = self.client.post(url, data=payload, header=header)
        return response

    def update_post(self, id: int, payload: Dict, header: Dict) -> HttpResponse:
        url = reverse('api-blog:detail', kwargs={'pk': id})
        response = self.client.put(url, data=payload, header=header)
        return response

    def delete_post(self, id: int, header: Dict) -> HttpResponse:
        url = reverse('api-blog:detail', kwargs={'pk': id})
        response = self.client.delete(url, header=header)
        return response

    def get_token(self, username: str = 'user1', password: str = 'passuser1', logout: bool = False) -> Dict:
        if logout:
            self.client.logout()
        url = reverse('rest_login')
        payload = {'username': username, 'password': password}
        response = self.client.post(url, data=payload, )
        token = response.json().get('key')
        header = {'Authorization': f'Token {token}'}
        return header

    def test_no_authorization_post_list_view(self):
        """ Testing `PostListView` without any authorization """
        response = self.get_response_post_list_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @login_by_session
    def test_athorization_post_list_view(self):
        """ Testing `PostListView` with authorization """
        response = self.get_response_post_list_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_no_authorizatin_post_detail_view(self):
        """ Testing `PostDetailView` without any authorization """
        response = self.get_response_post_detail_view(id=self.post1.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @login_by_session
    def test_authorizatin_post_detail_view(self):
        """ Testing `PostDetailView` without any authorization """
        response = self.get_response_post_detail_view(id=self.post1.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_post_with_token(self):
        payload = {
            'title': 'title',
            'body': 'body',
            'reading_time': 300
        }
        header = self.get_token()
        response = self.create_post(payload, header)
        id_ = response.json().get('id')
        post = Post.objects.get(id=id_)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(post.author, self.user1)
        self.assertEqual(post.title, 'title')
        self.assertEqual(post.body, 'body')
        self.assertEqual(post.reading_time, timedelta(seconds=300))
        self.assertEqual(Post.objects.count(), 2)

    def test_update_post_with_token(self):
        payload = {
            'title': 'title',
            'body': 'body',
            'reading_time': 300
        }
        header = self.get_token()

        response = self.create_post(payload, header)
        id_ = response.json().get('id')
        post = Post.objects.get(id=id_)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(post.author, self.user1)
        self.assertEqual(post.title, 'title')
        self.assertEqual(post.body, 'body')
        self.assertEqual(post.reading_time, timedelta(seconds=300))
        self.assertEqual(Post.objects.count(), 2)

        payload_update = {
            'title': 'title updated',
            'body': 'body updated',
            'reading_time': 600
        }
        response = self.update_post(id_, payload_update, header)
        post = Post.objects.get(id=id_)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(post.author, self.user1)
        self.assertEqual(post.title, 'title updated')
        self.assertEqual(post.body, 'body updated')
        self.assertEqual(post.reading_time, timedelta(seconds=600))
        self.assertEqual(Post.objects.count(), 2)

    def test_delete_post_with_token(self):
        header = self.get_token()
        response = self.delete_post(2, header)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Post.objects.count(), 1)

    def test_delete_post_with_diffrent_author(self):
        payload = {
            'title': 'title',
            'body': 'body',
            'reading_time': 300
        }
        header = self.get_token(username='user1', password='passuser1')
        response = self.create_post(payload, header)
        id_ = response.json().get('id')
        post = Post.objects.get(id=id_)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(post.author, self.user1)
        self.assertEqual(post.title, 'title')
        self.assertEqual(post.body, 'body')
        self.assertEqual(post.reading_time, timedelta(seconds=300))
        self.assertEqual(Post.objects.count(), 2)

        # try to delete
        header = self.get_token(
            username='user2', password='passuser2', logout=True)
        response = self.delete_post(post.id, header)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotEqual(Post.objects.count(), 1)

    def test_update_post_with_diffrent_author(self):
        payload = {
            'title': 'title',
            'body': 'body',
            'reading_time': 300
        }
        header = self.get_token(username='user1', password='passuser1')
        response = self.create_post(payload, header)
        id_ = response.json().get('id')
        post = Post.objects.get(id=id_)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(post.author, self.user1)
        self.assertEqual(post.title, 'title')
        self.assertEqual(post.body, 'body')
        self.assertEqual(post.reading_time, timedelta(seconds=300))
        self.assertEqual(Post.objects.count(), 2)

        # try to update
        payload = {
            'title': 'title updated',
            'body': 'body updated',
            'reading_time': 500
        }
        header = self.get_token(
            username='user2', password='passuser2', logout=True)
        response = self.update_post(post.id, payload, header)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
