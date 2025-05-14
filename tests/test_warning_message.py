import pytest
from unittest import mock
from messages_managers.warning import WarningMessage

@pytest.fixture
def mock_text_manager():
    with mock.patch("messages_managers.warning.TextManager.color") as mock_color:
        yield mock_color

def test_action_cancelled(mock_text_manager):
    WarningMessage.action_cancelled()
    mock_text_manager.assert_called_once_with("Action annulée.", "yellow")

def test_cancel_command_info(mock_text_manager):
    WarningMessage.cancel_command_info()
    mock_text_manager.assert_called_once_with("(Appuyez sur Ctrl+C pour annuler)", "yellow")

def test_empty_table(mock_text_manager):
    WarningMessage.empty_table("TestTable")
    mock_text_manager.assert_called_once_with("La table 'TestTable' est vide.", "yellow")

def test_no_table_update(mock_text_manager):
    WarningMessage.no_table_update()
    mock_text_manager.assert_called_once_with("Toutes les tables sont déjà à jour.", "yellow")