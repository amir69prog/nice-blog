from typing import Dict

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status


User = get_user_model()


class SessionAuthUserTests(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            phone_number='09127777777',
            username='username1',
            email='username_email@gmail.com',
            first_name='username_first_name',
            last_name='username_last_name',
            password='123456789',
        )

    def login(self):
        self.client.login(phone_number='09127777777', password='123456789')

    def test_user_content(self):
        self.assertEqual(self.user.phone_number, '09127777777')
        self.assertEqual(self.user.username, 'username1')
        self.assertEqual(self.user.email, 'username_email@gmail.com')
        self.assertEqual(self.user.first_name, 'username_first_name')
        self.assertEqual(self.user.last_name, 'username_last_name')

    def test_user_list_view(self):
        url = reverse('api-user:list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_detail_view(self):
        url = reverse('api-user:detail', args=(self.user.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_list_view_authorized(self):
        self.login()
        url = reverse('api-user:list')
        response = self.client.get(url)
        self.assertEqual(response.status_code,
                         status.HTTP_403_FORBIDDEN)  # not verified
        self.assertEqual(response.json(), {
                         'detail': 'Your account is not verified.'})

    def test_user_detail_view_authorized(self):
        self.login()
        url = reverse('api-user:detail', args=(self.user.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code,
                         status.HTTP_403_FORBIDDEN)  # not verified
        self.assertEqual(response.json(), {
                         'detail': 'Your account is not verified.'})


class TokenAuthUserTests(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            phone_number='09127777777',
            username='username1',
            email='username_email@gmail.com',
            first_name='username_first_name',
            last_name='username_last_name',
            password='123456789',
        )
        self.user2 = User.objects.create_user(
            phone_number='09212222222',
            username='username2',
            email='username2_email@gmail.com',
            first_name='username2_first_name',
            last_name='username2_last_name',
            password='123456789',
        )

    def authenticate(self, phone_number: str, password: str):
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

    def test_user_list_view_authorized(self):
        access_key = self.authenticate('09127777777', '123456789')
        url = reverse('api-user:list')
        response = self.client.get(url, HTTP_AUTHORIZATION=access_key)
        self.assertEqual(response.status_code,
                         status.HTTP_403_FORBIDDEN)  # not verified
        self.assertEqual(response.json(), {
                         'detail': 'Your account is not verified.'})

    def test_user_detail_view_authorized(self):
        access_key = self.authenticate('09127777777', '123456789')
        url = reverse('api-user:detail', args=(self.user.id,))
        response = self.client.get(url, HTTP_AUTHORIZATION=access_key)
        self.assertEqual(response.status_code,
                         status.HTTP_403_FORBIDDEN)  # not verified
        self.assertEqual(response.json(), {
                         'detail': 'Your account is not verified.'})

    def test_verified_user_list_view(self):
        self.user.is_verified = True
        self.user.save()
        access_key = self.authenticate('09127777777', '123456789')
        url = reverse('api-user:list')
        response = self.client.get(url, HTTP_AUTHORIZATION=access_key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_verified_user_detail_view(self):
        self.user.is_verified = True
        self.user.save()
        access_key = self.authenticate('09127777777', '123456789')
        url = reverse('api-user:detail', args=(self.user.id,))
        response = self.client.get(url, HTTP_AUTHORIZATION=access_key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user(self):
        self.user.is_verified = True
        self.user.save()
        access_key = self.authenticate('09127777777', '123456789')
        url = reverse('api-user:detail', args=(self.user.id,))
        payload = {
            "phone_number": "09127777777",
            "username": "username1",
            "email": "username1@gmail.com",
            "first_name": "first_name_username1",
            "last_name": "last_name_username1"
        }
        response = self.client.put(
            url, data=payload, HTTP_AUTHORIZATION=access_key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user1 = User.objects.filter(phone_number='09127777777').get()
        self.assertEqual(user1.phone_number, '09127777777')
        self.assertEqual(user1.username, 'username1')
        self.assertEqual(user1.email, 'username1@gmail.com')
        self.assertEqual(user1.first_name, 'first_name_username1')
        self.assertEqual(user1.last_name, 'last_name_username1')
        self.assertTrue(user1.is_verified)

    def test_update_different_user(self):
        self.user.is_verified = True
        self.user.save()
        access_key = self.authenticate('09127777777', '123456789')
        url = reverse('api-user:detail', args=(self.user2.id,))
        payload = {
            "phone_number": "09127777777",
            "username": "username1",
            "email": "username1@gmail.com",
            "first_name": "first_name_username1",
            "last_name": "last_name_username1"
        }
        response = self.client.put(
            url, data=payload, HTTP_AUTHORIZATION=access_key)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_registration_user_then_delete(self):
        url = reverse('api-user:signup')
        payload = {
            "phone_number": "09125555555",
            "username": "username3",
            "email": "username3_email@gmail.com",
            "password": "123456789",
            "password2": "123456789"
        }
        response = self.client.post(url, data=payload)
        user3 = User.objects.filter(phone_number='09125555555').get()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 3)

        self.assertEqual(user3.phone_number, '09125555555')
        self.assertEqual(user3.username, 'username3')
        self.assertEqual(user3.email, 'username3_email@gmail.com')
        self.assertEqual(user3.first_name, '')
        self.assertEqual(user3.last_name, '')
        self.assertFalse(user3.is_verified)

        user3.is_verified = True
        access_key = self.authenticate('09125555555', '123456789')
        url = reverse('api-user:detail', args=(user3.id,))
        response = self.client.delete(url, HTTP_AUTHORIZATION=access_key)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        user3.save()
        response = self.client.delete(url, HTTP_AUTHORIZATION=access_key)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 2)
