# tests/test_collab_manager.py
import pytest
import uuid
from unittest.mock import patch, MagicMock
from models_managers.collab import CollaborateurManager
from models import Collaborateur, Role
from datetime import datetime

@pytest.fixture
def user_mock():
    user = MagicMock()
    user.id = uuid.uuid4()
    user.role = "Gestion"
    return user

@pytest.fixture
def db_manager_mock(session):
    mock = MagicMock()
    mock.session_scope.return_value.__enter__.return_value = session
    mock.update_commit = MagicMock()
    return mock

def create_gestion(session, user_id):
    gestion = Collaborateur(
        id=user_id,
        nom="Test Gestion",
        email="test.gestion@test.com",
        password_hash="fakepassword",
        role_id=2
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

def test_get_collab(db_manager_mock, user_mock, session):
    create_role(session, "Commercial")
    collab = create_gestion(session, user_mock.id)

    manager = CollaborateurManager(db_manager_mock, user_mock)
    with patch("builtins.input", side_effect=["test.gestion@test.com"]):
        result = manager.get_collaborateur(session)

        assert result is not None
        assert result.nom == collab.nom
        assert result.email == collab.email

def test_create_collab(db_manager_mock, user_mock, session):
    create_role(session, "Commercial")

    manager = CollaborateurManager(db_manager_mock, user_mock)
    with patch("models_managers.collab.JWTManager.token_valid", return_value=True), \
        patch("models_managers.collab.Permission.collab_management", return_value=True), \
        patch("models_managers.user.Utils.get_questionnary", return_value="Commercial"), \
        patch("builtins.input", side_effect=["Dupont", "Dupont"]), \
        patch("pwinput.pwinput", return_value="fakepassword"):
        manager.create_collab()

        collab = session.query(Collaborateur).filter_by(email="dupont.dupont@epicevents.com").first()
        assert collab is not None
        assert collab.nom == "Dupont DUPONT"
        assert collab.email == "dupont.dupont@epicevents.com"

def test_delete_collab(db_manager_mock, user_mock, session):
    create_role(session, "Commercial")
    collab = create_gestion(session, user_mock.id)

    manager = CollaborateurManager(db_manager_mock, user_mock)
    with patch("models_managers.collab.JWTManager.token_valid", return_value=True), \
        patch("models_managers.collab.Permission.collab_management", return_value=True), \
        patch("models_managers.collab.Utils.confirm_deletion", return_value=True), \
        patch("models_managers.collab.Utils.new_screen"):
        manager.delete_collab(collab.id)

        deleted_collab = session.query(Collaborateur).filter_by(id=collab.id).first()
        assert deleted_collab is None
