from typing import Dict

from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.urls import reverse


from rest_framework.test import APITestCase
from rest_framework import status

from blog.models import Post


User = get_user_model()


class UserAPITests(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1', password='passuser1')
        self.user2 = User.objects.create_user(
            username='user2', password='passuser2')

    def login_by_session(test_func, username='user1', password='passuser1'):
        def wrapper(self):
            self.client.login(username=username, password=password)
            return test_func(self)
        return wrapper

    def get_response_user_list_view(self) -> HttpResponse:
        """ Return response for UserListView """
        url = reverse('api-user:list')
        response = self.client.get(url)
        return response

    def get_response_user_detail_view(self, id: int) -> HttpResponse:
        """ Return response for UserDetailView """
        url = reverse('api-user:detail', kwargs={'pk': id})
        response = self.client.get(url)
        return response

    def update_user(self, id: int, payload: Dict, header: Dict) -> HttpResponse:
        url = reverse('api-user:detail', kwargs={'pk': id})
        response = self.client.put(url, data=payload, header=header)
        return response

    def delete_user(self, id: int, header: Dict) -> HttpResponse:
        url = reverse('api-user:detail', kwargs={'pk': id})
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

    def test_no_authorization_user_list_view(self):
        """ Testing `UserListView` without any authorization """
        response = self.get_response_user_list_view()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @login_by_session
    def test_athorization_user_list_view(self):
        """ Testing `UserListView` with authorization """
        response = self.get_response_user_list_view()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_no_authorizatin_user_detail_view(self):
        """ Testing `UserDetailView` without any authorization """
        response = self.get_response_user_detail_view(id=self.user1.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user1_content(self):
        self.assertEqual(self.user1.username, 'user1')
        self.assertEqual(self.user1.first_name, '')
        self.assertEqual(self.user1.last_name, '')
        self.assertEqual(self.user1.email, '')

    @login_by_session
    def test_authorizatin_user_detail_view(self):
        """ Testing `UserDetailView` without any authorization """
        response = self.get_response_user_detail_view(id=self.user1.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user_with_token(self):
        payload = {
            'username': 'user1',
            'first_name': 'user1_first_name',
            'last_name': 'user1_last_name',
            'email': 'user1_email@gmail.com',
        }
        header = self.get_token()

        response = self.update_user(self.user1.id, payload, header)
        user = User.objects.get(id=self.user1.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(user.username, payload['username'])
        self.assertEqual(user.first_name, payload['first_name'])
        self.assertEqual(user.last_name, payload['last_name'])
        self.assertEqual(user.email, payload['email'])

    def test_update_user_with_token_diffrent_user(self):
        payload = {
            'first_name': 'user1_first_name',
            'last_name': 'user1_last_name',
            'email': 'user1_email@gmail.com'
        }
        header = self.get_token(username='user2', password='passuser2')

        response = self.update_user(self.user1.id, payload, header)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_post_with_token(self):
        header = self.get_token()
        response = self.delete_user(1, header)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 1)

    def test_user_post_with_token_diffrent_user(self):
        header = self.get_token(
            username='user2', password='passuser2', logout=True)
        # try to delete user1 with user2
        response = self.delete_user(self.user1.id, header)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(User.objects.count(), 2)
