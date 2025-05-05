import sentry_sdk
import pwinput

from models import Collaborateur
from .jwt_utils import JWTManager
from .password_security import PasswordSecurity
from messages_managers.error import ErrorMessage
from messages_managers.success import SuccessMessage
from messages_managers.warning import WarningMessage
from app.settings import ADMIN_PASSWORD


class AuthManager:
    @staticmethod
    def login(db_manager):
        JWTManager.delete_token()
        WarningMessage.cancel_command_info()

        with db_manager.session_scope() as session:
            try:
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
                        collaborateur = session.query(Collaborateur
                                                    ).filter_by(email=email
                                                                ).first()
                        if not collaborateur:
                            ErrorMessage.account_not_found()
                            continue
                    except Exception as e:
                        ErrorMessage.database_error()
                        sentry_sdk.capture_exception(e)
                        return
                    break

                # Mot de passe
                while True:
                    password = pwinput.pwinput(prompt="Mot de passe : ")
                    if not password:
                        ErrorMessage.password_empty()
                        continue
                    break
            except KeyboardInterrupt:
                WarningMessage.action_cancelled()
                return

            if (collaborateur
                and PasswordSecurity.verify(
                    password, collaborateur.password_hash.encode('utf-8')
                    )):
                token = JWTManager.create_token(
                    collaborateur.id,
                    collaborateur.nom,
                    collaborateur.role.nom
                )
                JWTManager.save_token(token)
            else:
                ErrorMessage.invalid_credentials()

    @staticmethod
    def login_admin():
        WarningMessage.cancel_command_info()
        while True:
            try:
                password = pwinput.pwinput(
                    prompt="Mot de passe (Administrateur): "
                    )
                if not password:
                    ErrorMessage.admin_password_empty()
                    continue
                if not PasswordSecurity.verify(password, ADMIN_PASSWORD):
                    ErrorMessage.admin_password_incorrect()
                    continue
                break
            except KeyboardInterrupt:
                WarningMessage.action_cancelled()
                return

    @staticmethod
    def logout():
        if JWTManager.token_exist():
            JWTManager.delete_token()
            SuccessMessage.logout_success()
