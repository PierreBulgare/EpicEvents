import pytest
from unittest import mock
from messages_managers.error import ErrorMessage

@pytest.fixture
def mock_text_manager():
    with mock.patch("messages_managers.error.TextManager.color") as mock_color:
        yield mock_color

@pytest.fixture
def mock_print():
    with mock.patch("builtins.print") as mock_print:
        yield mock_print

def test_invalid_email(mock_text_manager, mock_print):
    text = "L'email fourni est invalide."
    mock_text_manager.return_value = text
    ErrorMessage.invalid_email()
    mock_text_manager.assert_called_once_with(text, "red")
    mock_print.assert_called_once_with(text)


def test_email_empty(mock_text_manager, mock_print):
    text = "L'email ne peut pas être vide."
    mock_text_manager.return_value = text
    ErrorMessage.email_empty()
    mock_text_manager.assert_called_once_with(text, "red")
    mock_print.assert_called_once_with(text)


def test_collab_already_exists(mock_text_manager, mock_print):
    text = "Le collaborateur John existe déjà."
    mock_text_manager.return_value = text
    ErrorMessage.collab_already_exists("John")
    mock_text_manager.assert_called_once_with(text, "red")
    mock_print.assert_called_once_with(text)


def test_client_email_already_exists(mock_text_manager, mock_print):
    text = "L'email client@test.com est déjà utilisé pour un autre client."
    mock_text_manager.return_value = text
    ErrorMessage.client_email_already_exists("client@test.com")
    mock_text_manager.assert_called_once_with(text, "red")
    mock_print.assert_called_once_with(text)


def test_client_not_assigned_to_user_edit(mock_text_manager, mock_print):
    text = "Vous devez être assigné à ce client pour le modifier."
    mock_text_manager.return_value = text
    ErrorMessage.client_not_assigned_to_user(edit=True)
    mock_text_manager.assert_called_once_with(text, "red")
    mock_print.assert_called_once_with(text)


def test_client_not_assigned_to_user_delete(mock_text_manager, mock_print):
    text = "Vous devez être assigné à ce client pour le supprimer."
    mock_text_manager.return_value = text
    ErrorMessage.client_not_assigned_to_user(delete=True)
    mock_text_manager.assert_called_once_with(text, "red")
    mock_print.assert_called_once_with(text)


def test_contract_not_assigned_to_user_to_create_evt(mock_text_manager, mock_print):
    text = "Vous devez être assigné au client lié à ce contrat pour créer un événement."
    mock_text_manager.return_value = text
    ErrorMessage.contract_not_assigned_to_user_to_create_evt()
    mock_text_manager.assert_called_once_with(text, "red")
    mock_print.assert_called_once_with(text)


def test_contract_not_signed_for_event(mock_text_manager, mock_print):
    text = "Le contrat n'est pas signé, vous ne pouvez pas encore créer d'évènement."
    mock_text_manager.return_value = text
    ErrorMessage.contract_not_signed_for_event()
    mock_text_manager.assert_called_once_with(text, "red")
    mock_print.assert_called_once_with(text)


def test_username_empty(mock_text_manager, mock_print):
    text = "Vous n'avez pas renseigné votre nom."
    mock_text_manager.return_value = text
    ErrorMessage.username_empty()
    mock_text_manager.assert_called_once_with(text, "red")
    mock_print.assert_called_once_with(text)


def test_user_firstname_empty(mock_text_manager, mock_print):
    text = "Vous n'avez pas renseigné votre prénom."
    mock_text_manager.return_value = text
    ErrorMessage.user_firstname_empty()
    mock_text_manager.assert_called_once_with(text, "red")
    mock_print.assert_called_once_with(text)


def test_password_empty(mock_text_manager, mock_print):
    text = "Le mot de passe ne peut pas être vide."
    mock_text_manager.return_value = text
    ErrorMessage.password_empty()
    mock_text_manager.assert_called_once_with(text, "red")
    mock_print.assert_called_once_with(text)


def test_password_too_short(mock_text_manager, mock_print):
    text = "Le mot de passe doit contenir au moins 8 caractères."
    mock_text_manager.return_value = text
    ErrorMessage.password_too_short()
    mock_text_manager.assert_called_once_with(text, "red")
    mock_print.assert_called_once_with(text)


def test_invalid_token(mock_text_manager, mock_print):
    text = "Le token est invalide ou a expiré."
    mock_text_manager.return_value = text
    ErrorMessage.invalid_token()
    mock_text_manager.assert_called_once_with(text, "red")
    mock_print.assert_called_once_with(text)


def test_token_not_found(mock_text_manager, mock_print):
    text = "Token introuvable. Vous devez vous connecter."
    mock_text_manager.return_value = text
    ErrorMessage.token_not_found()
    mock_text_manager.assert_called_once_with(text, "red")
    mock_print.assert_called_once_with(text)


def test_action_not_recognized(mock_text_manager, mock_print):
    text = "Action non reconnue. Veuillez réessayer."
    mock_text_manager.return_value = text
    ErrorMessage.action_not_recognized()
    mock_text_manager.assert_called_once_with(text, "red")
    mock_print.assert_called_once_with(text)


def test_database_error(mock_text_manager, mock_print):
    text = "Erreur de base de données. Veuillez réessayer."
    mock_text_manager.return_value = text
    ErrorMessage.database_error()
    mock_text_manager.assert_called_once_with(text, "red")
    mock_print.assert_called_once_with(text)


def test_account_not_found(mock_text_manager, mock_print):
    test_email = "inconnnu@epicevents.com"
    text = f"Aucun compte trouvé avec l'email : {test_email}."
    mock_text_manager.return_value = text
    ErrorMessage.account_not_found(test_email)
    mock_text_manager.assert_called_once_with(text, "red")
    mock_print.assert_called_once_with(text)


def test_data_not_found(mock_text_manager, mock_print):
    data_type = "Test"
    data_value = "test_data"
    text = f"{data_type} '{data_value}' introuvable. Veuillez vérifier les informations fournies."
    mock_text_manager.return_value = text
    ErrorMessage.data_not_found(data_type, data_value)
    mock_text_manager.assert_called_once_with(text, "red")
    mock_print.assert_called_once_with(text)


def test_table_not_found(mock_text_manager, mock_print):
    table_name = "TestTable"
    text = f"La table '{table_name}' n'existe pas."
    mock_text_manager.return_value = text
    ErrorMessage.table_not_found(table_name)
    mock_text_manager.assert_called_once_with(text, "red")
    mock_print.assert_called_once_with(text)


def test_tables_already_exists(mock_text_manager, mock_print):
    text = "Les tables existent déjà."
    mock_text_manager.return_value = text
    ErrorMessage.tables_already_exist()
    mock_text_manager.assert_called_once_with(text, "red")
    mock_print.assert_called_once_with(text)


def test_session_close_error(mock_text_manager, mock_print):
    error = Exception("Test error")
    text = f"Erreur lors de la fermeture de la session : {error}"
    mock_text_manager.return_value = text
    ErrorMessage.session_close_error(error)
    mock_text_manager.assert_called_once_with(text, "red")
    mock_print.assert_called_once_with(text)


def test_account_already_exists(mock_text_manager, mock_print):
    text = "Un compte existe déjà avec cet email."
    mock_text_manager.return_value = text
    ErrorMessage.account_already_exists()
    mock_text_manager.assert_called_once_with(text, "red")
    mock_print.assert_called_once_with(text)


def test_invalid_credentials(mock_text_manager, mock_print):
    text = "Email ou mot de passe incorrect."
    mock_text_manager.return_value = text
    ErrorMessage.invalid_credentials()
    mock_text_manager.assert_called_once_with(text, "red")
    mock_print.assert_called_once_with(text)


def test_role_not_found(mock_text_manager, mock_print):
    role_name = "RoleTest"
    text = f"Rôle '{role_name}' introuvable."
    mock_text_manager.return_value = text
    ErrorMessage.role_not_found(role_name)
    mock_text_manager.assert_called_once_with(text, "red")
    mock_print.assert_called_once_with(text)


def test_role_already_exists(mock_text_manager, mock_print):
    role_name = "RoleTest"
    text = f"Le rôle '{role_name}' existe déjà."
    mock_text_manager.return_value = text
    ErrorMessage.role_already_exists(role_name)
    mock_text_manager.assert_called_once_with(text, "red")
    mock_print.assert_called_once_with(text)


def test_role_empty(mock_text_manager, mock_print):
    text = "Le nom du rôle ne peut pas être vide."
    mock_text_manager.return_value = text
    ErrorMessage.role_empty()
    mock_text_manager.assert_called_once_with(text, "red")
    mock_print.assert_called_once_with(text)


def test_invalid_role(mock_text_manager, mock_print):
    ROLES = ["Commercial", "Gestion", "Support"]
    text = f"Rôle invalide. Veuillez choisir parmi : {', '.join(ROLES)}"
    mock_text_manager.return_value = text
    ErrorMessage.invalid_role()
    mock_text_manager.assert_called_once_with(text, "red")
    mock_print.assert_called_once_with(text)
