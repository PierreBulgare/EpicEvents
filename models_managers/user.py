import sentry_sdk
import pwinput
from models import Collaborateur, Role
from utils.jwt_utils import JWTManager
from utils.password_security import PasswordSecurity
from messages_managers.error import ErrorMessage
from messages_managers.success import SuccessMessage
from messages_managers.warning import WarningMessage
from .database import DatabaseManager


class UserManager:
    def __init__(self):
        pass

    def init_user(self, token, payload):
        self.id = payload.get("user_id")
        self.name = payload.get("user_name")
        self.role = payload.get("user_role")
        self.token = token
        self.payload = payload

    @staticmethod
    def create_account(db_manager: DatabaseManager):
        """
        Crée un compte collaborateur.
        """
        JWTManager.delete_token()
        WarningMessage.cancel_command_info()

        with db_manager.session_scope() as session:
            # Prénom
            while True:
                prenom = input("Prénom : ")
                if not prenom:
                    ErrorMessage.user_firstname_empty()
                    continue
                break

            # Nom
            while True:
                nom_de_famille = input("Nom : ")
                if not nom_de_famille:
                    ErrorMessage.username_empty()
                    continue
                nom = f"{prenom} {nom_de_famille.upper()}"
                break

            # Email
            while True:
                email = input("Email : ")
                if not email:
                    ErrorMessage.email_empty()
                    continue
                if "@" not in email or "." not in email.split("@")[-1]:
                    ErrorMessage.invalid_email()
                    continue
                try:
                    collaborateur = session.query(
                        Collaborateur
                    ).filter_by(email=email).first()
                except Exception as e:
                    ErrorMessage.database_error()
                    sentry_sdk.capture_exception(e)
                    continue
                if collaborateur:
                    ErrorMessage.account_already_exists()
                    continue
                break

            # Rôle
            while True:
                role_nom = input(
                    "Rôle (Commercial, Gestion, Support) : "
                ).capitalize()
                if not role_nom:
                    ErrorMessage.role_empty()
                    continue
                try:
                    role = session.query(Role).filter_by(nom=role_nom).first()
                except Exception as e:
                    ErrorMessage.database_error()
                    sentry_sdk.capture_exception(e)
                    continue
                if not role:
                    ErrorMessage.invalid_role()
                    continue
                break

            # Mot de passe
            while True:
                password = pwinput.pwinput(prompt="Mot de passe : ")
                if not password:
                    ErrorMessage.password_empty()
                    continue
                if len(password) < 8:
                    ErrorMessage.password_too_short()
                    continue
                break

            # Création du collaborateur
            new_collaborateur = Collaborateur(
                email=email,
                password_hash=PasswordSecurity.hash(password),
                nom=nom,
                role=role
            )
            session.add(new_collaborateur)
            session.commit()
            SuccessMessage.account_created()
