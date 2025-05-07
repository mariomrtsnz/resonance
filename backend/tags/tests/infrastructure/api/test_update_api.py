from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.infrastructure.persistence.models import User
from ....infrastructure.persistence.models import Skill as SkillModel
from uuid import uuid4

class SkillUpdateAPIViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@user.com', password='password123')
        self.admin_user = User.objects.create_superuser(username='adminuser', email='admin@user.com', password='adminpassword123')
        
        self.skill_to_update = SkillModel.objects.create(name="InitialSkillName")
        self.update_url = reverse('tags_api:skill-detail', kwargs={'pk': str(self.skill_to_update.id)})
        
        self.updated_data = {'name': 'UpdatedSkillName'}

    def test_update_skill_authenticated_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.put(self.update_url, self.updated_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.skill_to_update.refresh_from_db()
        self.assertEqual(self.skill_to_update.name, self.updated_data['name'])
        self.assertEqual(response.data['name'], self.updated_data['name'])
        self.assertEqual(response.data['id'], str(self.skill_to_update.id))

    def test_update_skill_authenticated_non_admin(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.put(self.update_url, self.updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.skill_to_update.refresh_from_db()
        self.assertNotEqual(self.skill_to_update.name, self.updated_data['name'])

    def test_update_skill_unauthenticated(self):
        response = self.client.put(self.update_url, self.updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.skill_to_update.refresh_from_db()
        self.assertNotEqual(self.skill_to_update.name, self.updated_data['name'])

    def test_update_skill_not_found(self):
        self.client.force_authenticate(user=self.admin_user)
        not_found_url = reverse('tags_api:skill-detail', kwargs={'pk': str(uuid4())})
        response = self.client.put(not_found_url, self.updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_skill_new_name_already_exists(self):
        SkillModel.objects.create(name="ExistingOtherSkill")
        self.client.force_authenticate(user=self.admin_user)
        
        conflicting_data = {'name': 'ExistingOtherSkill'}
        response = self.client.put(self.update_url, conflicting_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.data)
        self.assertIn('detail', response.data)
        self.assertTrue("already exists" in response.data['detail'])
        self.skill_to_update.refresh_from_db()
        self.assertNotEqual(self.skill_to_update.name, conflicting_data['name'])

    def test_update_skill_empty_name(self):
        self.client.force_authenticate(user=self.admin_user)
        empty_name_data = {'name': ''}
        response = self.client.put(self.update_url, empty_name_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)
        self.assertEqual(response.data['name'][0], 'Skill name cannot be empty')

    def test_update_skill_missing_name(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.put(self.update_url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)
        self.assertEqual(response.data['name'][0], 'Skill name is required')