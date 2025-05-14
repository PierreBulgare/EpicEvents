import pytest
import jwt
import os
from datetime import datetime, timedelta, timezone
from app.settings import JWT_SECRET_KEY, TOKEN_PATH
from utils.jwt_utils import JWTManager
from messages_managers.error import ErrorMessage
from messages_managers.success import SuccessMessage

@pytest.fixture
def mock_token_path(tmp_path, monkeypatch):
    # Utilise un fichier temporaire pour le fichier .token
    token_file = tmp_path / ".token"
    monkeypatch.setattr("app.settings.TOKEN_PATH", str(token_file))
    return str(token_file)

def test_create_token():
    token = JWTManager.create_token("123", "TestUser", "Commercial", expire_minutes=1)
    assert token is not None

def test_save_and_get_token(mock_token_path):
    token = JWTManager.create_token("123", "TestUser", "Commercial")
    JWTManager.save_token(token)
    saved_token = JWTManager.get_token()
    assert saved_token == token

def test_delete_token(mock_token_path):
    token = JWTManager.create_token("123", "TestUser", "Commercial")
    JWTManager.save_token(token)
    JWTManager.delete_token()
    assert JWTManager.get_token() is None

def test_token_exist(mock_token_path):
    assert not JWTManager.token_exist()
    token = JWTManager.create_token("123", "TestUser", "Commercial")
    JWTManager.save_token(token)
    assert JWTManager.token_exist()

def test_get_payload_valid_token():
    token = JWTManager.create_token("123", "TestUser", "Commercial", expire_minutes=1)
    payload = JWTManager.get_payload(token)
    assert payload is not None
    assert payload.get("user_id") == "123"
    assert payload.get("user_name") == "TestUser"
    assert payload.get("user_role") == "Commercial"

def test_get_payload_expired_token():
    token = JWTManager.create_token("123", "TestUser", "Commercial", expire_minutes=-1)
    payload = JWTManager.get_payload(token)
    assert payload is None

def test_verifier_role_valid_token():
    token = JWTManager.create_token("123", "TestUser", "Commercial", expire_minutes=1)
    assert JWTManager.verifier_role(token, "Commercial")
    assert not JWTManager.verifier_role(token, "user")

def test_token_valid_valid(mock_token_path):
    token = JWTManager.create_token("123", "TestUser", "Commercial")
    JWTManager.save_token(token)
    user = type("User", (), {"payload": JWTManager.get_payload(token)})
    assert JWTManager.token_valid(user)

def test_token_valid_invalid(mock_token_path):
    user = type("User", (), {"payload": None})
    assert not JWTManager.token_valid(user)
