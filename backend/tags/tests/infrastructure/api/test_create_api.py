from uuid import UUID
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.infrastructure.persistence.models import User
from ....infrastructure.persistence.models import Skill as SkillModel

class SkillCreateAPIViewTests(APITestCase):
    def setUp(self):
        self.create_url = reverse('tags_api:skill-list')
        
        self.user = User.objects.create_user(username='testuser', email='test@user.com', password='password123')
        self.admin_user = User.objects.create_superuser(username='adminuser', email='admin@user.com', password='adminpassword123')

        self.skill_data = {'name': 'NewSkill'}

    def test_create_skill_authenticated_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(self.create_url, self.skill_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(SkillModel.objects.count(), 1)
        created_skill = SkillModel.objects.get(name=self.skill_data['name'])
        
        self.assertIn('id', response.data)
        self.assertEqual(response.data['name'], self.skill_data['name'])
        self.assertEqual(UUID(response.data['id']), created_skill.id)

    def test_create_skill_authenticated_non_admin(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.create_url, self.skill_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(SkillModel.objects.count(), 0)

    def test_create_skill_unauthenticated(self):
        response = self.client.post(self.create_url, self.skill_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(SkillModel.objects.count(), 0)

    def test_create_skill_missing_name(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(self.create_url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)
        self.assertEqual(response.data['name'][0], 'Skill name is required')
        self.assertEqual(SkillModel.objects.count(), 0)

    def test_create_skill_empty_name(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(self.create_url, {'name': ''}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)
        self.assertEqual(response.data['name'][0], 'Skill name cannot be empty')
        self.assertEqual(SkillModel.objects.count(), 0)
        
    def test_create_skill_name_already_exists(self):
        SkillModel.objects.create(name='ExistingSkill')
        self.client.force_authenticate(user=self.admin_user)
        
        data = {'name': 'ExistingSkill'}
        response = self.client.post(self.create_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.data)
        self.assertIn('detail', response.data)
        self.assertTrue("already exists" in response.data['detail'])
        self.assertEqual(SkillModel.objects.count(), 1)