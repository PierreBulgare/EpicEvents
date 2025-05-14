import pytest
from utils.utils import Utils


@pytest.fixture(autouse=True)
def mock_get_questionnary(mocker):
    return mocker.patch("utils.utils.Utils.get_questionnary", delete=True)

def test_confirm_deletion_confirmer(mock_get_questionnary):
    mock_get_questionnary.return_value = "Confirmer"
    assert Utils.confirm_deletion() == True

def test_confirm_deletion_annuler(mock_get_questionnary):
    mock_get_questionnary.return_value = "Annuler"
    assert Utils.confirm_deletion() == False

def test_email_is_valid():
    assert Utils.email_is_valid("wrongemail.com") == False
    assert Utils.email_is_valid("wrongemail@com") == False
    assert Utils.email_is_valid("wrongemail@com.") == False
    assert Utils.email_is_valid("correctmail@domain.com") == True

def test_date_is_valid():
    assert Utils.date_is_valid("15-05-2025") == True
    assert Utils.date_is_valid("2025-05-15") == False
    assert Utils.date_is_valid("15/05/2025") == False

def test_generate_password():
    password = Utils.generate_password(12)
    assert len(password) == 12
    assert any(char.isdigit() for char in password)
    assert any(char.isalpha() for char in password)

def test_quit_app():
    with pytest.raises(SystemExit):
        Utils.quit_app()
