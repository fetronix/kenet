from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class UserAuthTests(TestCase):

    def test_register(self):
        response = self.client.post(reverse('register'), {
            'username': 'testuser',
            'password1': 'password123',
            'password2': 'password123'
        })
        self.assertEqual(response.status_code, 302)  # Check redirect after success
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_login(self):
        User.objects.create_user(username='testuser', password='password123')
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 302)  # Check for redirect on success
        self.assertTrue(response.wsgi_request.user.is_authenticated)
