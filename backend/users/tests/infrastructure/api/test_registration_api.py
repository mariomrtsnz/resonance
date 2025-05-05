from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.infrastructure.persistence.models import User, UserProfile

class UserRegistrationAPIViewTests(APITestCase):

    def setUp(self):
        self.register_url = reverse('users_api:register') 
        self.user_data = {
            'email': 'test@example.com',
            'password': 'GoodPassword123',
            'password2': 'GoodPassword123'
        }

    def test_successful_registration(self):
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(UserProfile.objects.count(), 1)
        
        registered_user = User.objects.select_related('profile').get(email='test@example.com')
        self.assertEqual(registered_user.email, 'test@example.com')
        self.assertEqual(registered_user.username, 'test@example.com')
        self.assertTrue(registered_user.check_password('GoodPassword123'))
        self.assertIsNotNone(registered_user.profile)
        
        self.assertEqual(response.data['email'], registered_user.email)
        self.assertEqual(response.data['username'], registered_user.username)
        self.assertEqual(str(response.data['id']), str(registered_user.id))

    def test_registration_mismatched_passwords(self):
        self.user_data['password2'] = 'wrongpassword'
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(UserProfile.objects.count(), 0)
        self.assertIn('password', response.data)
        self.assertEqual(response.data['password'][0], "Password fields didn't match.")

    def test_registration_existing_email(self):
        existing_user = User.objects.create_user(username='test@example.com', email='test@example.com', password='password123')
        UserProfile.objects.create(user=existing_user)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(UserProfile.objects.count(), 1)

        data = {
            'email': self.user_data['email'],
            'password': 'newpassword123',
            'password2': 'newpassword123'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(UserProfile.objects.count(), 1)
        self.assertIn('error', response.data)
        self.assertTrue(response.data['error'].startswith("User with email"))
        self.assertTrue(response.data['error'].endswith("already exists."))

    def test_registration_missing_email(self):
        del self.user_data['email']
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(UserProfile.objects.count(), 0)
        self.assertIn('email', response.data)
        self.assertEqual(response.data['email'][0], 'This field is required.')

    def test_registration_missing_password(self):
        del self.user_data['password']
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(UserProfile.objects.count(), 0)
        self.assertIn('password', response.data)
        self.assertEqual(response.data['password'][0], 'This field is required.')

    def test_registration_missing_password2(self):
        del self.user_data['password2']
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(UserProfile.objects.count(), 0)
        self.assertIn('password2', response.data)
        self.assertEqual(response.data['password2'][0], 'This field is required.')
        
    def test_registration_short_password(self):
        self.user_data['password'] = 'short'
        self.user_data['password2'] = 'short'
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(UserProfile.objects.count(), 0)
        self.assertIn('password', response.data)
        self.assertTrue("Ensure this field has at least 8 characters." in response.data['password'][0]) 