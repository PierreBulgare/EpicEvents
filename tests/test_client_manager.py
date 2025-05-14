# tests/test_client_manager.py
import pytest
import uuid
from unittest import mock
from unittest.mock import patch, MagicMock
from models_managers.client import ClientManager
from models import Client
from models import Collaborateur
from datetime import datetime

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

def create_commercial(session, user_id):
    commercial = Collaborateur(
        id=user_id,
        nom="Test Commercial",
        email="test@epicevents.com",
        password_hash="fakepassword",
        role_id=1
    )
    session.add(commercial)
    session.commit()
    return commercial


@patch("models_managers.client.JWTManager.token_valid", return_value=True)
@patch("models_managers.client.Permission.client_management", return_value=True)
@patch("models_managers.client.Utils.new_screen")
@patch("builtins.input", side_effect=[
    "Dupont Dupont",         # nom_complet
    "dupont@dupont.com", # email
    "+1 674 782 987",       # téléphone
    "Entreprise"          # entreprise
])
@patch("models_managers.client.Utils.get_questionnary", return_value="🔙 Retour")
@patch("models_managers.client.SuccessMessage.create_success")
def test_create_client(
    mock_success, mock_questionary, mock_input, mock_screen,
    mock_permission, mock_token,
    db_manager_mock, user_mock, session
):
    create_commercial(session, user_mock.id)

    manager = ClientManager(db_manager_mock, user_mock)
    manager.create_client()

    from models import Client

    client = session.query(Client).filter_by(email="dupont@dupont.com").first()
    assert client is not None
    assert client.nom_complet == "Dupont Dupont"
    assert client.nom_entreprise == "Entreprise"

@patch("models_managers.client.Utils.get_input", side_effect=[
    "Paul Martin",              # Nouveau nom complet
    "paul.martin@test.com",     # Nouvel email
    "06 12 34 56 78",           # Nouveau téléphone
    "Nouvelle Entreprise"       # Nouveau nom d'entreprise
])
@patch("models_managers.client.Utils.get_questionnary", side_effect=["Tout modifier", "Retour"])
@patch("models_managers.client.Utils.new_screen")
@patch("models_managers.client.Permission.client_management", return_value=True)
@patch("models_managers.client.JWTManager.token_valid", return_value=True)
def test_update_client_tout_modifier(
    mock_token, mock_permission, mock_screen,
    mock_questionary, mock_input,
    user_mock, session
):
    # Préparation des données
    commercial = create_commercial(session, user_mock.id)

    from models import Client
    from datetime import datetime

    client = Client(
        nom_complet="Jean Dupont",
        email="jd@example.com",
        telephone="0123456789",
        nom_entreprise="Entreprise X",
        date_creation=datetime.now(),
        derniere_maj=datetime.now(),
        commercial_id=commercial.id
    )
    session.add(client)
    session.commit()

    # db_manager simplifié
    class SimpleDBManager:
        def session_scope(self):
            class Scope:
                def __enter__(self_): return session
                def __exit__(self_, *args): pass
            return Scope()
        def update_commit(self, obj, sess):
            sess.commit()

    db_manager = SimpleDBManager()
    manager = ClientManager(db_manager, user_mock)

    # Exécution
    manager.update_client(client.id)

    session.refresh(client)
    assert client.nom_complet == "Paul Martin"
    assert client.email == "paul.martin@test.com"
    assert client.telephone == "06 12 34 56 78"
    assert client.nom_entreprise == "Nouvelle Entreprise"

@patch("models_managers.client.Utils.confirm_deletion", return_value=True)
@patch("models_managers.client.Utils.new_screen")
@patch("models_managers.client.Permission.client_management", return_value=True)
@patch("models_managers.client.JWTManager.token_valid", return_value=True)
@patch("models_managers.client.SuccessMessage.delete_success")
def test_delete_client(
    mock_success, mock_token, mock_permission, mock_screen, mock_confirm,
    user_mock, session
):
    # Préparation
    commercial = create_commercial(session, user_mock.id)

    from models import Client
    from datetime import datetime

    client = Client(
        nom_complet="Jean Dupont",
        email="jd@example.com",
        telephone="0123456789",
        nom_entreprise="Entreprise X",
        date_creation=datetime.now(),
        derniere_maj=datetime.now(),
        commercial_id=commercial.id
    )
    session.add(client)
    session.commit()

    # db_manager réel
    class SimpleDBManager:
        def session_scope(self):
            class Scope:
                def __enter__(self_): return session
                def __exit__(self_, *args): pass
            return Scope()

    db_manager = SimpleDBManager()
    manager = ClientManager(db_manager, user_mock)

    # Exécution
    manager.delete_client(client.id)

    client_after = session.query(Client).filter_by(id=client.id).first()
    assert client_after is None

def test_get_client(user_mock, session):
    commercial = create_commercial(session, user_mock.id)

    client = Client(
        nom_complet="Jean Dupont",
        email="jean.dupont@dupont.com",
        telephone="0123456789",
        nom_entreprise="Entreprise X",
        date_creation=datetime.now(),
        derniere_maj=datetime.now(),
        commercial_id=commercial.id
    )

    session.add(client)
    session.commit()

    manager = ClientManager(session, user_mock)
    with patch("builtins.input", return_value="jean.dupont@dupont.com"):
        result = manager.get_client(session)

    assert result is not None
    assert result.nom_complet == "Jean Dupont"

def test_display_all_clients(user_mock, session, db_manager_mock, capfd):
    commercial = create_commercial(session, user_mock.id)

    client1 = Client(
        nom_complet="Jean Dupont",
        email="jean.dupont@dupont.com",
        telephone="0123456789",
        nom_entreprise="Entreprise X",
        date_creation=datetime.now(),
        derniere_maj=datetime.now(),
        commercial_id=commercial.id
    )
    client2 = Client(
        nom_complet="Marie Curie",
        email="marie.curie@curie.com",
        telephone="9876543210",
        nom_entreprise="Entreprise B",
        date_creation=datetime.now(),
        derniere_maj=datetime.now(),
        commercial_id=commercial.id
    )
    session.add(client1)
    session.add(client2)
    session.commit()
    manager = ClientManager(db_manager_mock, user_mock)
    with patch("models_managers.client.Utils.new_screen", return_value=user_mock), \
        patch("models_managers.client.JWTManager.token_valid", return_value=True):
        manager.display_all_clients()
    
    captured = capfd.readouterr()
    output = captured.out

    # Vérification
    assert client1 in session.query(Client).all()
    assert client2 in session.query(Client).all()
    
    assert "Jean Dupont".ljust(20) in output
    assert "jean.dupont@dupont.com".ljust(30) in output
    assert "Marie Curie".ljust(20) in output
    assert "marie.curie@curie.com".ljust(30) in output
