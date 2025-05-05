import uuid
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.infrastructure.persistence.models import User
from ....infrastructure.persistence.models import Project

class ProjectCreateAPIViewTests(APITestCase):

    def setUp(self):
        self.url = reverse('projects_api:project-list-create')
        user_email = 'testuser@example.com'
        self.test_user = User.objects.create_user(
            username=user_email,
            email=user_email,
            password='testpassword123'
        )
        self.project_data = {
            'title': 'My Awesome Song',
            'description': 'Looking for a drummer for an R&B track.',
            'needed_skill_text': 'Drums, R&B genre experience'
        }
        self.client.force_authenticate(user=self.test_user)

    def test_create_project_authenticated(self):
        response = self.client.post(self.url, self.project_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        
        self.assertEqual(Project.objects.count(), 1)
        created_project = Project.objects.get(title=self.project_data['title'])
        
        self.assertIn('id', response.data)
        self.assertEqual(response.data['title'], self.project_data['title'])
        self.assertEqual(uuid.UUID(response.data['owner_id']), self.test_user.id)
        self.assertEqual(response.data['description'], self.project_data['description'])
        self.assertEqual(response.data['needed_skill_text'], self.project_data['needed_skill_text'])
        
        self.assertEqual(uuid.UUID(response.data['id']), created_project.id)
        self.assertEqual(created_project.owner, self.test_user)

    def test_create_project_unauthenticated(self):
        self.client.force_authenticate(user=None) 
        
        unauth_data = {
            'title': 'Secret Project',
            'description': 'Top secret stuff.',
            'needed_skill_text': 'Stealth'
        }
        response = self.client.post(self.url, unauth_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Project.objects.count(), 0)

    def test_create_project_missing_title(self):
        invalid_data = self.project_data.copy()
        del invalid_data['title']
        
        response = self.client.post(self.url, invalid_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Project.objects.count(), 0)
        self.assertIn('title', response.data) 
        self.assertEqual(response.data['title'][0], 'This field is required.')

    def test_create_project_optional_fields_blank(self):
        minimal_data = {
            'title': 'Minimal Project',
            'description': '',
            'needed_skill_text': ''
        }
        
        response = self.client.post(self.url, minimal_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(Project.objects.count(), 1)
        created_project = Project.objects.get(title=minimal_data['title'])
        
        self.assertEqual(response.data['title'], minimal_data['title'])
        self.assertIsNone(response.data['description'])
        self.assertIsNone(response.data['needed_skill_text'])
        self.assertIsNone(created_project.description)
        self.assertIsNone(created_project.needed_skill_text)

    def test_create_project_optional_fields_null(self):
        null_data = {
            'title': 'Null Optional Fields Project',
            'description': None,
            'needed_skill_text': None
        }
        
        response = self.client.post(self.url, null_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(Project.objects.count(), 1)
        created_project = Project.objects.get(title=null_data['title'])
        
        self.assertEqual(response.data['title'], null_data['title'])
        self.assertIsNone(response.data['description'])
        self.assertIsNone(response.data['needed_skill_text'])
        self.assertIsNone(created_project.description)
        self.assertIsNone(created_project.needed_skill_text) 
