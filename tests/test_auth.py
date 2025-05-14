import pytest
from unittest import mock
from unittest.mock import patch
from utils.auth import AuthManager
from utils.jwt_utils import JWTManager
from messages_managers.error import ErrorMessage
from messages_managers.success import SuccessMessage
from messages_managers.warning import WarningMessage
from app.settings import ADMIN_PASSWORD
from models import Collaborateur
from utils.password_security import PasswordSecurity

@pytest.fixture
def mock_db_manager():
    class MockSession:
        def __init__(self):
            self.kwargs = {}

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            pass

        def query(self, model):
            return self

        def filter_by(self, **kwargs):
            self.kwargs = kwargs
            return self

        def first(self):
            email = self.kwargs.get("email")
            if email == "collab@epicevents.com":
                mock_collaborateur = Collaborateur()
                mock_collaborateur.id = 1
                mock_collaborateur.nom = "TestCollab"
                mock_collaborateur.email = email
                
                mock_collaborateur.password_hash = PasswordSecurity.hash("correct_password").decode('utf-8')
                mock_collaborateur.role = type("Role", (), {"nom": "Commercial"})
                return mock_collaborateur
            else:
                return None

    class MockDBManager:
        def session_scope(self):
            return MockSession()

    return MockDBManager()

@mock.patch("utils.jwt_utils.JWTManager.delete_token")
@mock.patch("utils.jwt_utils.JWTManager.save_token")
@mock.patch("builtins.input", side_effect=["inconnu@epicevents.com"])
def test_login_user_not_found(mock_input, mock_save_token, mock_delete_token, mock_db_manager):
    AuthManager.login(mock_db_manager)

    assert mock_delete_token.called
    assert not mock_save_token.called

@mock.patch("pwinput.pwinput", side_effect=["wrong_admin_password", "correct_admin_password"])
def test_login_admin(mock_pwinput):
    with patch("utils.password_security.PasswordSecurity.verify", side_effect=[False, True]):
        AuthManager.login_admin()

        assert mock_pwinput.call_count == 2

@mock.patch("utils.jwt_utils.JWTManager.delete_token")
@mock.patch("utils.jwt_utils.JWTManager.token_exist", return_value=True)
def test_logout(mock_token_exist, mock_delete_token):
    with mock.patch("messages_managers.success.SuccessMessage.logout_success") as mock_success_message:
        AuthManager.logout()

        mock_token_exist.assert_called_once()
        mock_delete_token.assert_called_once()
        mock_success_message.assert_called_once()