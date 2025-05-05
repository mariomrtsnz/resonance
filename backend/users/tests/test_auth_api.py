from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.infrastructure.persistence.models import User, UserProfile

class UserAuthTests(APITestCase):
    def setUp(self):
        """Set up test data."""
        self.login_url = reverse('users_api:token_obtain_pair')
        self.refresh_url = reverse('users_api:token_refresh')

        self.user_email = 'testlogin@example.com'
        self.user_password = 'password123'
        self.user = User.objects.create_user(username=self.user_email, email=self.user_email, password=self.user_password)
        UserProfile.objects.create(user=self.user)

    def test_login_success(self):
        """Ensure registered user can log in and receive tokens."""
        login_data = {'username': self.user_email, 'password': self.user_password}
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_failure_wrong_password(self):
        """Ensure login fails with incorrect password."""
        login_data = {'username': self.user_email, 'password': 'wrongpassword'}
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, response.data)
        self.assertNotIn('access', response.data)
        self.assertNotIn('refresh', response.data)
        self.assertEqual(response.data['detail'], 'No active account found with the given credentials')

    def test_login_failure_nonexistent_user(self):
        """Ensure login fails for a user that does not exist."""
        login_data = {'username': 'nosuchuser@example.com', 'password': 'password123'}
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, response.data)
        self.assertNotIn('access', response.data)
        self.assertNotIn('refresh', response.data)
        self.assertEqual(response.data['detail'], 'No active account found with the given credentials')

    def test_token_refresh_success(self):
        """Ensure a user can refresh their access token using a valid refresh token."""
        login_data = {'username': self.user_email, 'password': self.user_password}
        login_response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(login_response.status_code, status.HTTP_200_OK, login_response.data)
        self.assertTrue('refresh' in login_response.data)
        refresh_token = login_response.data['refresh']

        refresh_data = {'refresh': refresh_token}
        refresh_response = self.client.post(self.refresh_url, refresh_data, format='json')

        self.assertEqual(refresh_response.status_code, status.HTTP_200_OK)
        self.assertIn('access', refresh_response.data)
        # Refresh token might or might not be returned depending on SIMPLE_JWT settings
        # self.assertIn('refresh', refresh_response.data) 

    def test_token_refresh_failure_invalid_token(self):
        """Ensure token refresh fails with an invalid or expired refresh token."""
        refresh_data = {'refresh': 'thisisclearlyaninvalidtoken'}
        response = self.client.post(self.refresh_url, refresh_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)
        self.assertIn('code', response.data)
        self.assertEqual(response.data['code'], 'token_not_valid') 