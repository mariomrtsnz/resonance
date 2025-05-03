from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegistrationAPIViewTests(APITestCase):

    def setUp(self):
        self.register_url = reverse('register')
        self.user_data = {
            'email': 'test@example.com',
            'password': 'password123',
            'password2': 'password123'
        }

    def test_successful_registration(self):
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(User.objects.count(), 1)
        registered_user = User.objects.get(email='test@example.com')
        self.assertEqual(registered_user.email, 'test@example.com')
        self.assertTrue(registered_user.check_password('password123'))
        # Check the actual success message returned by the view
        self.assertEqual(response.data, {"message": "User registered successfully."})


    def test_registration_mismatched_passwords(self):
        self.user_data['password2'] = 'wrongpassword'
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)
        # Check error is on the 'password' field key as per serializer logic
        self.assertIn('password', response.data)
        self.assertEqual(response.data['password'][0], "Password fields didn't match.")

    def test_registration_existing_email(self):
        User.objects.create_user(username=self.user_data['email'], email=self.user_data['email'], password='password123')
        self.assertEqual(User.objects.count(), 1)

        data = {
            'email': self.user_data['email'],
            'password': 'newpassword',
            'password2': 'newpassword'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertIn('email', response.data)
        # Check the exact validation error message from the serializer
        self.assertEqual(response.data['email'][0], "A user with that email already exists.")

    def test_registration_missing_email(self):
        del self.user_data['email']
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)
        self.assertIn('email', response.data)
        self.assertEqual(response.data['email'][0], 'This field is required.')


    def test_registration_missing_password(self):
        del self.user_data['password']
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)
        self.assertIn('password', response.data)
        self.assertEqual(response.data['password'][0], 'This field is required.')


    def test_registration_missing_password2(self):
        del self.user_data['password2']
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)
        self.assertIn('password2', response.data)
        self.assertEqual(response.data['password2'][0], 'This field is required.') 