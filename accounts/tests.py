from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import resolve, reverse

from .views import user_profile_view


User = get_user_model()


class BlogTests(TestCase):
    
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            phone_number='09121212121',
            username='testuser',
            email='testuser@gmail.com',
            password='123456789',
            is_verified=True
        )

    def login(self):
        self.client.login(phone_number='09121212121', password='123456789')

    def test_profile_view(self):
        self.login()

        url = reverse('accounts:profile')
        view = resolve(url)
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Profile')
        self.assertTemplateUsed(response, 'accounts/profile.html')
        self.assertEqual(view.func.__name__, user_profile_view.__name__)