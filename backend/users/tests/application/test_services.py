import uuid
import unittest
from unittest.mock import MagicMock, patch, ANY

from users.application.services import UserService, UserRegistrationError
from users.application.dtos import UserRegistrationDTO, UserDTO
from users.domain.entities import User as DomainUser
from users.domain.repositories import AbstractUserRepository

class UserServiceTests(unittest.TestCase):

    def setUp(self):
        self.mock_user_repository = MagicMock(spec=AbstractUserRepository)
        self.user_service = UserService(user_repository=self.mock_user_repository)
        
        self.test_email = "test@example.com"
        self.test_password = "password123"
        self.test_user_id = uuid.uuid4()
        self.registration_dto = UserRegistrationDTO(email=self.test_email, password=self.test_password)
        self.domain_user = DomainUser(
            id=self.test_user_id, 
            email=self.test_email, 
            username=self.test_email
        )
        self.user_dto = UserDTO(
            id=self.test_user_id, 
            email=self.test_email, 
            username=self.test_email
        )

    @patch('users.application.services.make_password')
    def test_register_user_success(self, mock_make_password):
        hashed_password = "hashed_password"
        mock_make_password.return_value = hashed_password
        self.mock_user_repository.get_by_email.return_value = None
        self.mock_user_repository.add.return_value = self.domain_user

        result_dto = self.user_service.register_user(self.registration_dto)

        self.mock_user_repository.get_by_email.assert_called_once_with(self.test_email)
        mock_make_password.assert_called_once_with(self.test_password)
        self.mock_user_repository.add.assert_called_once()
        call_args, _ = self.mock_user_repository.add.call_args
        added_user_arg = call_args[0]
        added_password_arg = call_args[1]
        
        self.assertIsInstance(added_user_arg, DomainUser)
        self.assertEqual(added_user_arg.email, self.test_email)
        self.assertEqual(added_user_arg.username, self.test_email)
        self.assertEqual(added_password_arg, hashed_password)
        
        self.assertEqual(result_dto, self.user_dto)

    def test_register_user_email_exists(self):
        self.mock_user_repository.get_by_email.return_value = self.domain_user

        with self.assertRaises(UserRegistrationError) as cm:
            self.user_service.register_user(self.registration_dto)
        
        self.assertTrue(f"User with email {self.test_email} already exists." in str(cm.exception))
        self.mock_user_repository.get_by_email.assert_called_once_with(self.test_email)
        self.mock_user_repository.add.assert_not_called()

    def test_get_user_by_id_found(self):
        self.mock_user_repository.get_by_id.return_value = self.domain_user

        result_dto = self.user_service.get_user_by_id(self.test_user_id)

        # 
        self.mock_user_repository.get_by_id.assert_called_once_with(self.test_user_id)
        self.assertEqual(result_dto, self.user_dto)

    def test_get_user_by_id_not_found(self):
        self.mock_user_repository.get_by_id.return_value = None

        result_dto = self.user_service.get_user_by_id(self.test_user_id)

        self.mock_user_repository.get_by_id.assert_called_once_with(self.test_user_id)
        self.assertIsNone(result_dto)

    def test_get_user_by_email_found(self):
        self.mock_user_repository.get_by_email.return_value = self.domain_user

        result_dto = self.user_service.get_user_by_email(self.test_email)

        self.mock_user_repository.get_by_email.assert_called_once_with(self.test_email)
        self.assertEqual(result_dto, self.user_dto)

    def test_get_user_by_email_not_found(self):
        self.mock_user_repository.get_by_email.return_value = None 

        result_dto = self.user_service.get_user_by_email(self.test_email)

        self.mock_user_repository.get_by_email.assert_called_once_with(self.test_email)
        self.assertIsNone(result_dto)

if __name__ == '__main__':
    unittest.main()
