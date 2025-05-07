from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.infrastructure.persistence.models import User
from ....infrastructure.persistence.models import Skill as SkillModel

class SkillListAPIViewTests(APITestCase):

    def setUp(self):
        self.list_url = reverse('tags_api:skill-list')
        
        self.user = User.objects.create_user(username='testuser', email='test@user.com', password='password123')
        self.admin_user = User.objects.create_superuser(username='adminuser', email='admin@user.com', password='adminpassword123')

        self.skill1 = SkillModel.objects.create(name="Python")
        self.skill2 = SkillModel.objects.create(name="Django")

    def test_list_skills_unauthenticated(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_skills_authenticated_non_admin(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_list_skills_authenticated_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_list_skills_contains_correct_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        skill1_data = next((item for item in response.data if item['id'] == str(self.skill1.id)), None)
        skill2_data = next((item for item in response.data if item['id'] == str(self.skill2.id)), None)

        self.assertIsNotNone(skill1_data)
        self.assertEqual(skill1_data['name'], self.skill1.name)
        
        self.assertIsNotNone(skill2_data)
        self.assertEqual(skill2_data['name'], self.skill2.name)

    def test_list_skills_no_skills(self):
        SkillModel.objects.all().delete()
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
        self.assertEqual(response.data, [])