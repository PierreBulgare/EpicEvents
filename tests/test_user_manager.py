import pytest
from unittest.mock import MagicMock, patch
from models_managers.user import UserManager
from utils.password_security import PasswordSecurity
from models import Collaborateur, Role
import uuid

from datetime import datetime, timedelta

@pytest.fixture
def user_mock():
    user = MagicMock()
    user.id = uuid.uuid4()
    user.role = "Commercial"
    return user

@pytest.fixture
def db_manager_mock(session):
    mock = MagicMock()
    mock.session_scope.return_value.__enter__.return_value = session
    mock.update_commit = MagicMock()
    return mock

def create_commercial(session):
    commercial = Collaborateur(
        nom="Test Commercial",
        email="test@epicevents.com",
        password_hash = PasswordSecurity.hash("fakepassword"),
        role_id=1
    )
    session.add(commercial)
    session.commit()
    return commercial

def create_support(session, user_id):
    support = Collaborateur(
        id=user_id,
        nom="Test Support",
        email="support@test.com",
        password_hash="fakepassword",
        role_id=2
    )
    session.add(support)
    session.commit()
    return support

def create_gestion(session, user_id):
    gestion = Collaborateur(
        id=user_id,
        nom="Test Gestion",
        email="gestion@test.com",
        password_hash="fakepassword",
        role_id=3
    )
    session.add(gestion)
    session.commit()
    return gestion

def create_role(session, role_name):
    role = Role(
        nom=role_name
    )
    session.add(role)
    session.commit()
    return role

def test_user_exists(db_manager_mock, user_mock, session):
    collab = create_commercial(session)
    
    manager = UserManager()
    manager.id = collab.id
    with patch("models_managers.user.DatabaseManager.session_scope", return_value=session):
        result = manager.user_exists()

    assert result is True

def test_create_account(db_manager_mock, user_mock, session):
    create_role(session, "Commercial")
    with patch("models_managers.user.Utils.get_questionnary", return_value="Commercial"), \
        patch("builtins.input", side_effect=["Dupont", "Dupont"]), \
        patch("pwinput.pwinput", return_value="fakepassword"):
        manager = UserManager()
        manager.create_account(db_manager_mock)
        collab = session.query(Collaborateur).filter_by(email="dupont.dupont@epicevents.com").first()
        assert collab is not None
        assert collab.nom == "Dupont DUPONT"
        assert collab.email == "dupont.dupont@epicevents.com"
