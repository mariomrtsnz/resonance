from uuid import uuid4
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.infrastructure.persistence.models import User
from ....infrastructure.persistence.models import Skill as SkillModel

class SkillRetrieveAPIViewTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@user.com', password='password123')
        self.admin_user = User.objects.create_superuser(username='adminuser', email='admin@user.com', password='adminpassword123')
        
        self.skill = SkillModel.objects.create(name="TestSkill")
        self.retrieve_url = reverse('tags_api:skill-detail', kwargs={'pk': str(self.skill.id)})
        self.not_found_url = reverse('tags_api:skill-detail', kwargs={'pk': str(uuid4())})

    def test_retrieve_skill_unauthenticated(self):
        response = self.client.get(self.retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_skill_authenticated_non_admin(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], str(self.skill.id))

    def test_retrieve_skill_authenticated_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], str(self.skill.id))

    def test_retrieve_skill_not_found(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.not_found_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('detail', response.data)

    def test_retrieve_skill_invalid_uuid_format(self):
        invalid_uuid_url = reverse('tags_api:skill-detail', kwargs={'pk': "not-a-uuid"})
        self.client.force_authenticate(user=self.user)
        response = self.client.get(invalid_uuid_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], "Invalid skill ID format.")