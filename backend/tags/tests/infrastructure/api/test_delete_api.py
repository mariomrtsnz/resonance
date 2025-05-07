from uuid import uuid4
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.infrastructure.persistence.models import User
from ....infrastructure.persistence.models import Skill as SkillModel

class SkillDeleteAPIViewTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@user.com', password='password123')
        self.admin_user = User.objects.create_superuser(username='adminuser', email='admin@user.com', password='adminpassword123')
        
        self.skill_to_delete = SkillModel.objects.create(name="SkillToDelete")
        self.delete_url = reverse('tags_api:skill-detail', kwargs={'pk': str(self.skill_to_delete.id)})

    def test_delete_skill_authenticated_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(self.delete_url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, response.data)
        self.assertFalse(SkillModel.objects.filter(id=self.skill_to_delete.id).exists())
        self.assertEqual(SkillModel.objects.count(), 0)

    def test_delete_skill_authenticated_non_admin(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(SkillModel.objects.filter(id=self.skill_to_delete.id).exists())

    def test_delete_skill_unauthenticated(self):
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(SkillModel.objects.filter(id=self.skill_to_delete.id).exists())

    def test_delete_skill_not_found(self):
        self.client.force_authenticate(user=self.admin_user)
        not_found_url = reverse('tags_api:skill-detail', kwargs={'pk': str(uuid4())})
        response = self.client.delete(not_found_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(SkillModel.objects.filter(id=self.skill_to_delete.id).exists())

    def test_delete_skill_invalid_uuid_format(self):
        self.client.force_authenticate(user=self.admin_user)
        invalid_uuid_url = reverse('tags_api:skill-detail', kwargs={'pk': "not-a-uuid"})
        response = self.client.delete(invalid_uuid_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], "Invalid skill ID format.")