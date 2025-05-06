import uuid
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.infrastructure.persistence.models import User
from ....infrastructure.persistence.models import Project

class ProjectRetrieveAPIViewTests(APITestCase):
    def setUp(self):
        user_email = 'testuser@example.com'
        self.test_user = User.objects.create_user(
            username=user_email,
            email=user_email,
            password='testpassword123'
        )
        self.project = Project.objects.create(
            owner=self.test_user,
            title="Test Project",
            description="Test Description",
            needed_skill_text="Test Skill"
        )

        self.url = reverse('projects_api:project-retrieve', kwargs={'pk': self.project.id})        

        other_user_email = 'otheruser@example.com'
        self.other_user = User.objects.create_user(
            username=other_user_email,
            email=other_user_email,
            password='otherpass123'
        )

    def test_retrieve_project_success(self):
        self.client.force_authenticate(user=self.test_user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(response.data['id'], str(self.project.id))
        self.assertEqual(response.data['title'], self.project.title)
        self.assertEqual(response.data['description'], self.project.description)
        self.assertEqual(response.data['needed_skill_text'], self.project.needed_skill_text)
        self.assertEqual(uuid.UUID(response.data['owner_id']), self.test_user.id)

    def test_retrieve_project_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_project_not_found(self):
        self.client.force_authenticate(user=self.test_user)
        url = reverse('projects_api:project-retrieve', kwargs={'pk': uuid.uuid4()})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_project_other_user(self):
        # TODO: This is a temporary test, we will change this to expect a 403 error
        # when the project privacy settings/open to collaborators are implemented
        self.client.force_authenticate(user=self.other_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)