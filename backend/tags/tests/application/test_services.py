import unittest
from unittest.mock import MagicMock, ANY
from uuid import uuid4
from ...application.services import SkillService
from ...application.dtos import SkillCreateDTO, SkillUpdateDTO, SkillDTO
from ...domain.entities import Skill as DomainSkill
from ...domain.repositories import AbstractSkillRepository
from ...domain.exceptions import SkillNotFoundError, SkillAlreadyExistsError

class SkillServiceTests(unittest.TestCase):
    def setUp(self):
        self.mock_skill_repository = MagicMock(spec=AbstractSkillRepository)
        self.skill_service = SkillService(repository=self.mock_skill_repository)

        self.skill_id_1 = uuid4()
        self.skill_name_1 = "Python"
        self.domain_skill_1 = DomainSkill(id=self.skill_id_1, name=self.skill_name_1)
        self.skill_dto_1 = SkillDTO.from_entity(self.domain_skill_1)

        self.skill_id_2 = uuid4()
        self.skill_name_2 = "Django"
        self.domain_skill_2 = DomainSkill(id=self.skill_id_2, name=self.skill_name_2)
        self.skill_dto_2 = SkillDTO.from_entity(self.domain_skill_2)

    def test_get_all_skills(self):
        self.mock_skill_repository.get_all.return_value = [self.domain_skill_1, self.domain_skill_2]
        
        result_dtos = self.skill_service.get_all_skills()

        self.mock_skill_repository.get_all.assert_called_once()
        self.assertEqual(len(result_dtos), 2)
        self.assertIn(self.skill_dto_1, result_dtos)
        self.assertIn(self.skill_dto_2, result_dtos)

    def test_get_all_skills_empty(self):
        self.mock_skill_repository.get_all.return_value = []
        
        result_dtos = self.skill_service.get_all_skills()

        self.mock_skill_repository.get_all.assert_called_once()
        self.assertEqual(len(result_dtos), 0)

    def test_create_skill_success(self):
        create_dto = SkillCreateDTO(name="New Skill")
        new_skill_id = uuid4()
        created_domain_skill = DomainSkill(id=new_skill_id, name=create_dto.name)
        
        self.mock_skill_repository.get_by_name.return_value = None
        self.mock_skill_repository.add.return_value = created_domain_skill

        result_dto = self.skill_service.create_skill(create_dto)

        self.mock_skill_repository.get_by_name.assert_called_once_with(create_dto.name)
        self.mock_skill_repository.add.assert_called_once()
        
        # Check that the argument passed to add was a DomainSkill with the correct name
        call_args, _ = self.mock_skill_repository.add.call_args
        added_skill_arg = call_args[0]
        self.assertIsInstance(added_skill_arg, DomainSkill)
        self.assertEqual(added_skill_arg.name, create_dto.name)
        
        self.assertEqual(result_dto.id, new_skill_id)
        self.assertEqual(result_dto.name, create_dto.name)

    def test_create_skill_already_exists(self):
        create_dto = SkillCreateDTO(name=self.skill_name_1)
        self.mock_skill_repository.get_by_name.return_value = self.domain_skill_1

        with self.assertRaises(SkillAlreadyExistsError):
            self.skill_service.create_skill(create_dto)

        self.mock_skill_repository.get_by_name.assert_called_once_with(self.skill_name_1)
        self.mock_skill_repository.add.assert_not_called()

    def test_get_skill_by_id_found(self):
        self.mock_skill_repository.get_by_id.return_value = self.domain_skill_1

        result_dto = self.skill_service.get_skill_by_id(self.skill_id_1)

        self.mock_skill_repository.get_by_id.assert_called_once_with(self.skill_id_1)
        self.assertEqual(result_dto, self.skill_dto_1)

    def test_get_skill_by_id_not_found(self):
        unknown_id = uuid4()
        self.mock_skill_repository.get_by_id.return_value = None

        with self.assertRaises(SkillNotFoundError):
            self.skill_service.get_skill_by_id(unknown_id)
        
        self.mock_skill_repository.get_by_id.assert_called_once_with(unknown_id)

    def test_update_skill_success(self):
        update_dto = SkillUpdateDTO(name="Updated Python")
        updated_domain_skill = DomainSkill(id=self.skill_id_1, name=update_dto.name)

        self.mock_skill_repository.get_by_id.return_value = self.domain_skill_1
        self.mock_skill_repository.get_by_name.return_value = None # No other skill has the new name
        self.mock_skill_repository.update.return_value = updated_domain_skill

        result_dto = self.skill_service.update_skill(self.skill_id_1, update_dto)

        self.mock_skill_repository.get_by_id.assert_called_once_with(self.skill_id_1)
        self.mock_skill_repository.get_by_name.assert_called_once_with(update_dto.name)
        self.mock_skill_repository.update.assert_called_once()
        
        call_args, _ = self.mock_skill_repository.update.call_args
        updated_skill_arg = call_args[0]
        self.assertIsInstance(updated_skill_arg, DomainSkill)
        self.assertEqual(updated_skill_arg.id, self.skill_id_1)
        self.assertEqual(updated_skill_arg.name, update_dto.name)

        self.assertEqual(result_dto.id, self.skill_id_1)
        self.assertEqual(result_dto.name, update_dto.name)

    def test_update_skill_not_found(self):
        unknown_id = uuid4()
        update_dto = SkillUpdateDTO(name="Irrelevant Name")
        self.mock_skill_repository.get_by_id.return_value = None

        with self.assertRaises(SkillNotFoundError):
            self.skill_service.update_skill(unknown_id, update_dto)

        self.mock_skill_repository.get_by_id.assert_called_once_with(unknown_id)
        self.mock_skill_repository.get_by_name.assert_not_called()
        self.mock_skill_repository.update.assert_not_called()

    def test_update_skill_new_name_already_exists_for_different_skill(self):
        update_dto = SkillUpdateDTO(name=self.skill_name_2) # Trying to rename skill_1 to skill_2's name

        self.mock_skill_repository.get_by_id.return_value = self.domain_skill_1
        # Simulate that skill_name_2 already exists and belongs to domain_skill_2
        self.mock_skill_repository.get_by_name.return_value = self.domain_skill_2 

        with self.assertRaises(SkillAlreadyExistsError):
            self.skill_service.update_skill(self.skill_id_1, update_dto)

        self.mock_skill_repository.get_by_id.assert_called_once_with(self.skill_id_1)
        self.mock_skill_repository.get_by_name.assert_called_once_with(self.skill_name_2)
        self.mock_skill_repository.update.assert_not_called()

    def test_update_skill_name_unchanged(self):
        update_dto = SkillUpdateDTO(name=self.skill_name_1) # Name is the same
        # The updated domain skill will still have the same name
        updated_domain_skill = DomainSkill(id=self.skill_id_1, name=self.skill_name_1)


        self.mock_skill_repository.get_by_id.return_value = self.domain_skill_1
        # get_by_name should not be called if name is unchanged
        self.mock_skill_repository.update.return_value = updated_domain_skill

        result_dto = self.skill_service.update_skill(self.skill_id_1, update_dto)

        self.mock_skill_repository.get_by_id.assert_called_once_with(self.skill_id_1)
        self.mock_skill_repository.get_by_name.assert_not_called() # Crucial check
        self.mock_skill_repository.update.assert_called_once()
        
        self.assertEqual(result_dto.name, self.skill_name_1)


    def test_delete_skill_success(self):
        self.mock_skill_repository.get_by_id.return_value = self.domain_skill_1
        
        self.skill_service.delete_skill(self.skill_id_1)

        self.mock_skill_repository.get_by_id.assert_called_once_with(self.skill_id_1)
        self.mock_skill_repository.delete.assert_called_once_with(self.skill_id_1)

    def test_delete_skill_not_found(self):
        unknown_id = uuid4()
        self.mock_skill_repository.get_by_id.return_value = None

        with self.assertRaises(SkillNotFoundError):
            self.skill_service.delete_skill(unknown_id)

        self.mock_skill_repository.get_by_id.assert_called_once_with(unknown_id)
        self.mock_skill_repository.delete.assert_not_called()

    def test_get_skill_by_name_found(self):
        self.mock_skill_repository.get_by_name.return_value = self.domain_skill_1

        result_dto = self.skill_service.get_skill_by_name(self.skill_name_1)

        self.mock_skill_repository.get_by_name.assert_called_once_with(self.skill_name_1)
        self.assertEqual(result_dto, self.skill_dto_1)

    def test_get_skill_by_name_not_found(self):
        unknown_name = "UnknownSkill"
        self.mock_skill_repository.get_by_name.return_value = None

        with self.assertRaises(SkillNotFoundError):
            self.skill_service.get_skill_by_name(unknown_name)
        
        self.mock_skill_repository.get_by_name.assert_called_once_with(unknown_name)

if __name__ == '__main__':
    unittest.main()