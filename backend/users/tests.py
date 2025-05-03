from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegistrationAPIViewTests(APITestCase):

    def setUp(self):
        self.register_url = reverse('user-register')
        self.user_data = {
            'email': 'test@example.com',
            'password': 'password123',
            'password2': 'password123'
        }

    def test_successful_registration(self):
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'test@example.com')
        self.assertTrue(User.objects.get().check_password('password123'))
        self.assertEqual(response.data, {'message': 'User registered successfully.'})

    def test_registration_mismatched_passwords(self):
        self.user_data['password2'] = 'wrongpassword'
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)
        self.assertIn('password', response.data)
        self.assertEqual(response.data['password'][0], "Password fields didn't match.")

    def test_registration_existing_email(self):
        User.objects.create_user(username='existing@example.com', email='existing@example.com', password='password123')
        self.assertEqual(User.objects.count(), 1)

        data = {
            'email': 'existing@example.com', # Same email
            'password': 'newpassword',
            'password2': 'newpassword'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1) # Count should remain 1
        self.assertIn('email', response.data)
        # Default DRF unique validation message
        self.assertTrue('already exists' in response.data['email'][0])

    def test_registration_missing_email(self):
        del self.user_data['email']
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)
        self.assertIn('email', response.data)

    def test_registration_missing_password(self):
        del self.user_data['password']
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)
        self.assertIn('password', response.data)

    def test_registration_missing_password2(self):
        del self.user_data['password2']
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)
        self.assertIn('password2', response.data) 