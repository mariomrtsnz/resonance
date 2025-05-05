import unittest
from unittest.mock import Mock, patch, ANY
from uuid import uuid4, UUID
from datetime import datetime

from ...application.services import ProjectService
from ...application.dtos import ProjectCreateDTO, ProjectDTO
from ...domain.entities import Project
from ...domain.repositories import AbstractProjectRepository

class ProjectServiceTests(unittest.TestCase):

    def setUp(self):
        self.mock_project_repo = Mock(spec=AbstractProjectRepository)
        self.project_service = ProjectService(repository=self.mock_project_repo)

    def test_create_project_success(self):
        owner_id = uuid4()
        create_dto = ProjectCreateDTO(
            title="Test Project Title",
            description="Test description.",
            needed_skill_text="Python, Django"
        )
        
        created_project_entity = Project(
            id=uuid4(),
            owner_id=owner_id,
            title=create_dto.title,
            description=create_dto.description,
            needed_skill_text=create_dto.needed_skill_text,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        self.mock_project_repo.add.return_value = created_project_entity

        result_dto = self.project_service.create_project(project_data=create_dto, owner_id=owner_id)

        self.mock_project_repo.add.assert_called_once_with(ANY) 
        
        call_args, _ = self.mock_project_repo.add.call_args
        added_project_arg = call_args[0]
        self.assertIsInstance(added_project_arg, Project)
        self.assertEqual(added_project_arg.owner_id, owner_id)
        self.assertEqual(added_project_arg.title, create_dto.title)
        self.assertEqual(added_project_arg.description, create_dto.description)
        self.assertEqual(added_project_arg.needed_skill_text, create_dto.needed_skill_text)
        
        self.assertIsInstance(result_dto, ProjectDTO)
        self.assertEqual(result_dto.id, created_project_entity.id)
        self.assertEqual(result_dto.owner_id, created_project_entity.owner_id)
        self.assertEqual(result_dto.title, created_project_entity.title)
        self.assertEqual(result_dto.description, created_project_entity.description)
        self.assertEqual(result_dto.needed_skill_text, created_project_entity.needed_skill_text)
        self.assertEqual(result_dto.created_at, created_project_entity.created_at.isoformat())
        self.assertEqual(result_dto.updated_at, created_project_entity.updated_at.isoformat())

    def test_create_project_converts_blank_to_none(self):
        owner_id = uuid4()
        create_dto = ProjectCreateDTO(
            title="Test Blank Project",
            description="",
            needed_skill_text=""
        )
        
        created_project_entity = Project(
            id=uuid4(),
            owner_id=owner_id,
            title=create_dto.title,
            description=None,
            needed_skill_text=None,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        self.mock_project_repo.add.return_value = created_project_entity

        result_dto = self.project_service.create_project(project_data=create_dto, owner_id=owner_id)

        self.mock_project_repo.add.assert_called_once()
        call_args, _ = self.mock_project_repo.add.call_args
        added_project_arg = call_args[0]
        self.assertIsInstance(added_project_arg, Project)
        self.assertIsNone(added_project_arg.description)
        self.assertIsNone(added_project_arg.needed_skill_text)
        
        self.assertIsInstance(result_dto, ProjectDTO)
        self.assertIsNone(result_dto.description)
        self.assertIsNone(result_dto.needed_skill_text)
        self.assertEqual(result_dto.title, create_dto.title)

    def test_get_all_projects_success(self):
        project1 = Project(id=uuid4(), owner_id=uuid4(), title="P1", description="D1", needed_skill_text="S1", created_at=datetime.now(), updated_at=datetime.now())
        project2 = Project(id=uuid4(), owner_id=uuid4(), title="P2", description="D2", needed_skill_text="S2", created_at=datetime.now(), updated_at=datetime.now())
        mock_projects = [project1, project2]
        self.mock_project_repo.get_all.return_value = mock_projects

        result_dtos = self.project_service.get_all_projects()

        self.mock_project_repo.get_all.assert_called_once()
        self.assertEqual(len(result_dtos), 2)
        self.assertIsInstance(result_dtos[0], ProjectDTO)
        self.assertIsInstance(result_dtos[1], ProjectDTO)
        
        self.assertEqual(result_dtos[0].id, project1.id)
        self.assertEqual(result_dtos[0].title, project1.title)
        self.assertEqual(result_dtos[0].description, project1.description)
        self.assertEqual(result_dtos[0].needed_skill_text, project1.needed_skill_text)
        self.assertEqual(result_dtos[0].created_at, project1.created_at.isoformat())

    def test_get_all_projects_empty(self):
        self.mock_project_repo.get_all.return_value = []

        result_dtos = self.project_service.get_all_projects()

        self.mock_project_repo.get_all.assert_called_once()
        self.assertEqual(len(result_dtos), 0)
        self.assertEqual(result_dtos, [])

if __name__ == '__main__':
    unittest.main() 