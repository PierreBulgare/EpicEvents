from app.settings import JWT_SECRET_KEY, TOKEN_PATH
import jwt
import os
from datetime import datetime, timedelta, timezone
import sentry_sdk
from messages_managers.success import SuccessMessage
from messages_managers.error import ErrorMessage


class JWTManager:
    @staticmethod
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

    @staticmethod
    def delete_token():
        """
        Supprime le token JWT en vidant le fichier .token.
        """
        with open(TOKEN_PATH, "w") as f:
            f.truncate(0)

    @classmethod
    def get_token(cls):
        """
        Récupère le token JWT stocké dans le fichier .token.
        """
        if cls.token_exist():
            with open(TOKEN_PATH, "r") as f:
                return f.read().strip()
        return None

    @staticmethod
    def save_token(token):
        """
        Enregistre le token JWT dans le fichier .token.
        """
        with open(TOKEN_PATH, "w") as f:
            f.write(token)
        SuccessMessage.token_saved()

    @staticmethod
    def token_exist():
        """
        Vérifie s'il existe un token
        """
        return os.path.exists(TOKEN_PATH) and os.path.getsize(TOKEN_PATH) > 0

    @staticmethod
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

    @classmethod
    def verifier_role(cls, token, role):
        payload = cls.get_payload(token)
        if payload and payload.get("user_role") == role:
            return True
        return False

    @classmethod
    def token_valid(cls, user):
        if not cls.token_exist():
            ErrorMessage.token_not_found()
            return False
        
        if user.payload is None:
            ErrorMessage.invalid_token()
            return False
        
        return True
