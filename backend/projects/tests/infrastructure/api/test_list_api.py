import uuid
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.infrastructure.persistence.models import User
from ....infrastructure.persistence.models import Project

class ProjectListAPIViewTests(APITestCase):

    def setUp(self):
        self.url = reverse('projects_api:project-list-create')
        user_email = 'testuser@example.com'
        self.test_user = User.objects.create_user(
            username=user_email,
            email=user_email,
            password='testpassword123'
        )
        self.project1 = Project.objects.create(owner=self.test_user, title="Project Alpha")
        self.project2 = Project.objects.create(owner=self.test_user, title="Project Beta", description="Beta Desc")

        other_user_email = 'otheruser@example.com'
        self.other_user = User.objects.create_user(
            username=other_user_email,
            email=other_user_email,
            password='otherpass123'
        )
        self.project3 = Project.objects.create(owner=self.other_user, title="Project Gamma")

        self.client.force_authenticate(user=self.test_user)

    def test_list_projects_success(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(len(response.data), 3)

        response_titles = {p['title'] for p in response.data}
        expected_titles = {self.project1.title, self.project2.title, self.project3.title}
        self.assertEqual(response_titles, expected_titles)

        beta_data = next((p for p in response.data if p['id'] == str(self.project2.id)), None)
        self.assertIsNotNone(beta_data)
        self.assertEqual(beta_data['title'], self.project2.title)
        self.assertEqual(beta_data['description'], self.project2.description)
        self.assertIsNone(beta_data['needed_skill_text'])
        self.assertEqual(uuid.UUID(beta_data['owner_id']), self.test_user.id)

    def test_list_projects_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_projects_no_projects(self):
        Project.objects.all().delete()
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
        self.assertEqual(response.data, []) 
