import pytest
import uuid
from unittest.mock import patch, MagicMock
from models_managers.event import EventManager
from models_managers.contract import ContractManager
from models_managers.client import ClientManager
from models import Role
from models import Collaborateur, Client, Contrat, Evenement
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

@pytest.fixture
def role_support(session):
    print("✅ Initialisation de role_support")
    role = Role(id=2, nom="Support")
    session.add(role)
    session.commit()
    return role

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

def create_client(session, commercial_id):
    client = Client(
        nom_complet="Client Test",
        email="client@test.com",
        telephone="0123456789",
        nom_entreprise="TestEntreprise",
        date_creation=datetime.now(),
        derniere_maj=datetime.now(),
        commercial_id=commercial_id
    )
    session.add(client)
    session.commit()
    return client

def create_contract(session, client_id, commercial_id):
    contract = Contrat(
        client_id=client_id,
        montant_total=1000.0,
        montant_restant=1000.0,
        statut_signe=True,
        date_creation=datetime.now(),
        derniere_maj=datetime.now(),
        gestionnaire_id=commercial_id
    )
    session.add(contract)
    session.commit()
    return contract

def create_support(session, role):
    support = Collaborateur(
        id=uuid.uuid4(),
        nom="Support Collaborateur",
        email="support@epicevents.com",
        password_hash="fakepassword",
        role_id=role.id
    )
    support.role = role
    session.add(support)
    session.commit()
    return support

@patch("models_managers.event.JWTManager.token_valid", return_value=True)
@patch("models_managers.event.Permission.create_event", return_value=True)
@patch("models_managers.event.Utils.new_screen")
@patch("models_managers.event.EventManager.display_event")
def test_create_event(mock_display_event, mock_screen, mock_permission, mock_token, db_manager_mock, user_mock, session):
    commercial = create_commercial(session, user_mock.id)
    client = create_client(session, commercial.id)
    contract = create_contract(session, client.id, commercial.id)

    manager = EventManager(db_manager_mock, user_mock)

    with patch("builtins.input", side_effect=[
        str(contract.id),
        client.email,
        "Event Test",      # Nom de l'événement
        "15-05-2025",      # Date de début
        "16-05-2025",      # Date de fin
        "Paris",           # Lieu
        "50"               # Nombre de participants
    ]), patch("models_managers.event.SuccessMessage.create_success"):
        manager.create_event()

        event = session.query(Evenement).first()
        assert event is not None
        assert event.nom == "Event Test"
        assert event.lieu == "Paris"
        assert event.nombre_participants == 50
        assert event.contrat.id == contract.id

        mock_display_event.assert_called_once()

def test_delete_event(user_mock, session):
    commercial = create_commercial(session, user_mock.id)
    client = create_client(session, commercial.id)
    contract = create_contract(session, client.id, commercial.id)

    event = Evenement(
        nom="Event Test",
        date_debut=datetime.strptime("15-05-2025", "%d-%m-%Y"),
        date_fin=datetime.strptime("16-05-2025", "%d-%m-%Y"),
        lieu="Paris",
        nombre_participants=50,
        contrat_id=contract.id,
        date_creation=datetime.now()
    )
    session.add(event)
    session.commit()

    class SimpleDBManager:
        def session_scope(self):
            class Scope:
                def __enter__(self_): return session
                def __exit__(self_, *args): pass
            return Scope()

    db_manager = SimpleDBManager()

    manager = EventManager(db_manager, user_mock)

    with patch("models_managers.event.JWTManager.token_valid", return_value=True), \
        patch("models_managers.event.Utils.confirm_deletion", return_value=True), \
        patch("models_managers.event.Utils.new_screen"), \
        patch("models_managers.event.SuccessMessage.delete_success"), \
        patch("models_managers.event.ContractManager.get_contract", return_value=contract):

        manager.delete_event(event.id)

    event_after = session.query(Evenement).filter_by(id=event.id).first()
    assert event_after is None

def test_update_event(user_mock, session):
    commercial = create_commercial(session, user_mock.id)
    client = create_client(session, commercial.id)
    contract = Contrat(client_id=client.id, montant_total=1000.0, montant_restant=1000.0, statut_signe=True, date_creation=datetime.now(), derniere_maj=datetime.now(), gestionnaire_id=commercial.id)
    session.add(contract)
    session.commit()

    event = Evenement(
        nom="Event Test",
        date_debut=datetime.strptime("15-05-2025", "%d-%m-%Y"),
        date_fin=datetime.strptime("16-05-2025", "%d-%m-%Y"),
        lieu="Paris",
        nombre_participants=50,
        contrat_id=contract.id,
        date_creation=datetime.now(),
        derniere_maj=datetime.now()
    )
    session.add(event)
    session.commit()

    class SimpleDBManager:
        def session_scope(self):
            class Scope:
                def __enter__(self_): return session
                def __exit__(self_, exc_type, exc_value, traceback): pass
            return Scope()
        
        def update_commit(self, obj, session):
            session.commit()

    db_manager = SimpleDBManager()

    manager = EventManager(db_manager, user_mock)

    with patch("models_managers.event.Utils.new_screen", return_value=None), \
        patch("models_managers.event.JWTManager.token_valid", return_value=True), \
         patch("models_managers.event.Utils.get_questionnary", side_effect=["Tout modifier", "Retour"]), \
         patch("models_managers.event.Utils.get_input", side_effect=[
            "Event Test Updated",
            "16-05-2025",
            "17-05-2025",
            "Lyon",
            "100"
        ]):
        manager.update_event(event.id)

    event_after = session.query(Evenement).filter_by(id=event.id).first()
    assert event_after.nom == "Event Test Updated"
    assert event_after.date_debut.strftime("%d-%m-%Y") == "16-05-2025"
    assert event_after.date_fin.strftime("%d-%m-%Y") == "17-05-2025"
    assert event_after.lieu == "Lyon"
    assert event_after.nombre_participants == 100

def test_assign_event(user_mock, session, role_support):
    print("✅ Début du test assign_event")

    commercial = create_commercial(session, user_mock.id)
    client = create_client(session, commercial.id)
    contract = create_contract(session, client.id, commercial.id)

    event = Evenement(nom="Event Test", date_debut=datetime.now(), date_fin=datetime.now(), lieu="Paris", nombre_participants=50, contrat_id=contract.id, date_creation=datetime.now(), derniere_maj=datetime.now())
    session.add(event)
    session.commit()

    support = create_support(session, role_support)

    class SimpleDBManager:
        def session_scope(self):
            class Scope:
                def __enter__(self_): return session
                def __exit__(self_, exc_type, exc_value, traceback): pass
            return Scope()

        def update_commit(self, obj, session):
            session.commit()

    db_manager = SimpleDBManager()

    manager = EventManager(db_manager, user_mock)

    print("✅ Avant assign_event")

    with patch("models_managers.event.JWTManager.token_valid", return_value=True), \
         patch("models_managers.event.Permission.assign_event", return_value=True), \
         patch("models_managers.event.CollaborateurManager.get_collaborateur", return_value=support), \
         patch("models_managers.event.Utils.new_screen"), \
         patch("models_managers.event.SuccessMessage.assign_success"), \
         patch("models_managers.contract.Utils.get_questionnary", return_value="🔙 Retour"):

        print("✅ Appel de assign_event")
        manager.assign_event(event.id)
        print("✅ Fin de assign_event")

    event_after = session.query(Evenement).filter_by(id=event.id).first()

    print("Support ID après assignation:", event_after.support_id)

    assert event_after.support_id == support.id
    assert event_after.support.nom == "Support Collaborateur"
