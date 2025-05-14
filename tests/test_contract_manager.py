# tests/test_contract_manager.py
import pytest
import uuid
from unittest.mock import patch, MagicMock
from models_managers.contract import ContractManager
from models import Collaborateur, Client
from models import Contrat
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

@patch("models_managers.contract.JWTManager.token_valid", return_value=True)
@patch("models_managers.contract.Permission.contract_management", return_value=True)
@patch("models_managers.contract.Utils.new_screen")
@patch("builtins.input", side_effect=[
    "1500.00",             # Montant total
    "client@test.com"      # Email du client
])
@patch("models_managers.contract.Utils.get_questionnary", return_value="🔙 Retour")
@patch("models_managers.contract.SuccessMessage.create_success")
def test_create_contract(
    mock_success, mock_questionary, mock_input, mock_screen,
    mock_permission, mock_token,
    db_manager_mock, user_mock, session
):
    # Préparation des données en BDD
    commercial = create_commercial(session, user_mock.id)
    create_client(session, commercial.id)

    # Exécution
    manager = ContractManager(db_manager_mock, user_mock)
    manager.create_contract()

    from models import Contrat

    # Vérification
    contract = session.query(Contrat).first()
    assert contract is not None
    assert contract.montant_total == 1500.00
    assert contract.client.email == "client@test.com"
    assert contract.montant_restant == 1500.00

def test_sign_contract(user_mock, session):
    # Préparation des données
    commercial = create_commercial(session, user_mock.id)
    client = create_client(session, commercial.id)

    from models import Contrat
    from datetime import datetime, timedelta

    contract = Contrat(
        client=client,
        montant_total=1000.0,
        montant_restant=1000.0,
        date_creation=datetime.now() - timedelta(days=1),
        derniere_maj=datetime.now() - timedelta(days=1),
        gestionnaire=commercial
    )
    session.add(contract)
    session.commit()

    # Création d’un db_manager réel sans mock
    class SimpleDBManager:
        def session_scope(self):
            class Scope:
                def __enter__(self_): return session
                def __exit__(self_, *args): pass
            return Scope()

    db_manager = SimpleDBManager()

    manager = ContractManager(db_manager, user_mock)

    # Patch des fonctions externes
    with patch("models_managers.contract.JWTManager.token_valid", return_value=True), \
         patch("models_managers.contract.Utils.new_screen"), \
         patch("models_managers.contract.Utils.get_questionnary", return_value="🔙 Retour"), \
         patch("models_managers.contract.SuccessMessage.sign_success"):

        manager.sign_contract(contract.id)

    session.refresh(contract)
    assert contract.statut_signe is True
    assert contract.date_signature is not None

def test_delete_contract(user_mock, session):
    # Création des données nécessaires
    commercial = create_commercial(session, user_mock.id)
    client = create_client(session, commercial.id)

    from models import Contrat
    from datetime import datetime

    contract = Contrat(
        client=client,
        montant_total=500.0,
        montant_restant=500.0,
        date_creation=datetime.now(),
        derniere_maj=datetime.now(),
        gestionnaire=commercial
    )
    session.add(contract)
    session.commit()

    class SimpleDBManager:
        def session_scope(self):
            class Scope:
                def __enter__(self_): return session
                def __exit__(self_, *args): pass
            return Scope()

    db_manager = SimpleDBManager()

    manager = ContractManager(db_manager, user_mock)

    with patch("models_managers.contract.JWTManager.token_valid", return_value=True), \
        patch("models_managers.contract.Utils.confirm_deletion", return_value=True), \
        patch("models_managers.contract.Utils.new_screen"), \
        patch("models_managers.contract.SuccessMessage.delete_success"), \
        patch("models_managers.contract.ClientManager.get_client", return_value=client):

        manager.delete_contract(contract.id)

    contract_after = session.query(Contrat).filter_by(id=contract.id).first()
    assert contract_after is None

@patch("models_managers.contract.Utils.get_input", return_value="1500.0")
@patch("models_managers.contract.Utils.get_questionnary", side_effect=["Montant total", "Retour"])
@patch("models_managers.contract.Utils.new_screen")
@patch("models_managers.contract.Permission.contract_management", return_value=True)
@patch("models_managers.contract.JWTManager.token_valid", return_value=True)
def test_update_contract_total(
    mock_token, mock_permission, mock_screen,
    mock_questionary, mock_input,
    user_mock, session
):
    # Préparation des données
    commercial = create_commercial(session, user_mock.id)
    client = create_client(session, commercial.id)

    from models import Contrat
    from datetime import datetime

    contract = Contrat(
        client=client,
        montant_total=1000.0,
        montant_restant=1000.0,
        date_creation=datetime.now(),
        derniere_maj=datetime.now(),
        gestionnaire=commercial
    )
    session.add(contract)
    session.commit()

    # db_manager réel
    class SimpleDBManager:
        def session_scope(self):
            class Scope:
                def __enter__(self_): return session
                def __exit__(self_, *args): pass
            return Scope()
        def update_commit(self, obj, sess):  # pour éviter les erreurs
            sess.commit()

    db_manager = SimpleDBManager()

    manager = ContractManager(db_manager, user_mock)

    manager.update_contract(contract.id)

    session.refresh(contract)
    assert contract.montant_total == 1500.0
    assert contract.montant_restant == 1500.0

def test_update_montant_restant(user_mock, session):
    commercial = create_commercial(session, user_mock.id)
    client = create_client(session, commercial.id)

    from models import Contrat
    from datetime import datetime

    contract = Contrat(
        client=client,
        montant_total=1000.0,
        montant_restant=1000.0,
        date_creation=datetime.now(),
        derniere_maj=datetime.now(),
        gestionnaire=commercial
    )
    session.add(contract)
    session.commit()

    class SimpleDBManager:
        def session_scope(self):
            class Scope:
                def __enter__(self_): return session
                def __exit__(self_, *args): pass

            return Scope()
        
        def update_commit(self, obj, sess):  # pour éviter les erreurs
            sess.commit()

    db_manager = SimpleDBManager()
    manager = ContractManager(db_manager, user_mock)
    with patch("models_managers.contract.JWTManager.token_valid", return_value=True), \
            patch("models_managers.contract.Utils.get_questionnary", return_value="🔙 Retour"), \
            patch("models_managers.contract.Utils.get_input", return_value="500.0"), \
            patch("models_managers.contract.SuccessMessage.update_success"):
    
            manager.update_montant_restant(session, contract)

    session.refresh(contract)
    assert contract.montant_restant == 500.0
    assert contract.montant_total == 1000.0

def test_get_contract(user_mock, session):
    commercial = create_commercial(session, user_mock.id)
    client = create_client(session, commercial.id)

    from models import Contrat
    from datetime import datetime

    contract = Contrat(
        client=client,
        montant_total=1000.0,
        montant_restant=1000.0,
        date_creation=datetime.now(),
        derniere_maj=datetime.now(),
        gestionnaire=commercial
    )
    session.add(contract)
    session.commit()

    class SimpleDBManager:
        def session_scope(self):
            class Scope:
                def __enter__(self_): return session
                def __exit__(self_, *args): pass
            return Scope()

    db_manager = SimpleDBManager()

    manager = ContractManager(db_manager, user_mock)

    with patch("builtins.input", return_value=str(contract.id)):
        result = manager.get_contract(session)

    assert result is not None
    assert result.montant_total == 1000.0
    assert result.client.nom_complet == "Client Test"