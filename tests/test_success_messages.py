import pytest
from unittest import mock
from messages_managers.success import SuccessMessage

@pytest.fixture
def mock_text_manager():
    with mock.patch("messages_managers.warning.TextManager.color") as mock_color:
        yield mock_color

def test_create_success(mock_text_manager):
    SuccessMessage.create_success()
    mock_text_manager.assert_called_once_with("Création effectuée avec succès !", "green")

def test_collab_created(mock_text_manager):
    SuccessMessage.collab_created("Test")
    mock_text_manager.assert_called_once_with("Collaborateur Test créé avec succès !", "green")

def test_update_success(mock_text_manager):
    SuccessMessage.update_success()
    mock_text_manager.assert_called_once_with("Mise à jour effectuée avec succès !", "green")

def test_assign_success(mock_text_manager):
    SuccessMessage.assign_success("TestEvent", "TestSupport")
    mock_text_manager.assert_called_once_with("Assignation de l'événement TestEvent au support TestSupport ", "green")

def test_event_note_success(mock_text_manager):
    SuccessMessage.event_note_success()
    mock_text_manager.assert_called_once_with("Note ajoutée avec succès !", "green")

def test_delete_success(mock_text_manager):
    SuccessMessage.delete_success()
    mock_text_manager.assert_called_once_with("Suppression effectuée avec succès !", "green")

def test_logout_success(mock_text_manager):
    SuccessMessage.logout_success()
    mock_text_manager.assert_called_once_with("Vous êtes déconnecté avec succès !", "green")

def token_savved(mock_text_manager):
    SuccessMessage.token_savved()
    mock_text_manager.assert_called_once_with("Le token a été enregistré avec succès !", "green")

def test_table_created(mock_text_manager):
    SuccessMessage.table_created("TestTable")
    mock_text_manager.assert_called_once_with("La table 'TestTable' a été créée avec succès !", "green")

def test_tables_dropped(mock_text_manager):
    SuccessMessage.tables_dropped()
    mock_text_manager.assert_called_once_with("Les tables ont été supprimées avec succès !", "green")

def test_column_added(mock_text_manager):
    SuccessMessage.column_added("TestTable", "TestColumn")
    mock_text_manager.assert_called_once_with("La colonne 'TestColumn' a été ajoutée à la table 'TestTable' avec succès !", "green")

def test_role_createed(mock_text_manager):
    SuccessMessage.role_created("TestRole")
    mock_text_manager.assert_called_once_with("Le rôle 'TestRole' a été créé avec succès !", "green")

def test_sign_success(mock_text_manager):
    SuccessMessage.sign_success("12ad-54e7-8f3b-4c5e")
    mock_text_manager.assert_called_once_with("Le contrat 12ad-54e7-8f3b-4c5e a été signé avec succès !", "green")