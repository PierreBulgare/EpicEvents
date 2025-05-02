from settings import JWT_SECRET_KEY, TOKEN_PATH
import jwt
import os
from datetime import datetime, timedelta, timezone
import sentry_sdk
from managers.error_message import ErrorMessage


def create_token(user_id, user_name, user_role, expire_minutes=60):
    """
    Crée un token JWT pour l'utilisateur avec un ID et un rôle spécifiés.
    Le token expire après une heure.
    """
    payload = {
        "user_id": str(user_id),
        "user_name": user_name,
        "user_role": user_role,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=expire_minutes),
        "iat": datetime.now(timezone.utc)
    }

    return jwt.encode(payload, JWT_SECRET_KEY, algorithm="HS256")


def delete_token():
    """
    Supprime le token JWT en vidant le fichier .token.
    """
    with open(TOKEN_PATH, "w") as f:
        f.truncate(0)


def get_token():
    """
    Récupère le token JWT stocké dans le fichier .token.
    """
    if os.path.exists(TOKEN_PATH) and os.path.getsize(TOKEN_PATH) > 0:
        with open(TOKEN_PATH, "r") as f:
            return f.read().strip()
    return None


def save_token(token):
    """
    Enregistre le token JWT dans le fichier .token.
    """
    with open(TOKEN_PATH, "w") as f:
        f.write(token)
    print("Token enregistré avec succès !")


def token_exist():
    """
    Vérifie s'il existe un token
    """
    return os.path.getsize(TOKEN_PATH) != 0


def get_payload(token):
    """
    Récupère le payload du token JWT.
    """
    try:
        return jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError as e:
        sentry_sdk.capture_exception(e)
        return None
    except jwt.InvalidTokenError as e:
        sentry_sdk.capture_exception(e)
        return None


def verifier_role(token, role):
    payload = get_payload(token)
    if payload and payload.get("user_role") == role:
        return True
    return False


def token_valid(user):
    if not token_exist():
        ErrorMessage.token_not_found()
        return False
    
    if user.payload is None:
        ErrorMessage.invalid_token()
        return False
    
    return True
