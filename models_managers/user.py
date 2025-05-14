import sentry_sdk
import pwinput
from models import Collaborateur, Role
from utils.jwt_utils import JWTManager
from utils.password_security import PasswordSecurity
from utils.utils import Utils
from messages_managers.error import ErrorMessage
from messages_managers.success import SuccessMessage
from messages_managers.warning import WarningMessage
from .database import DatabaseManager
import slugify


class UserManager:
    def __init__(self):
        pass

    def init_user(self):
        token = JWTManager.get_token()
        payload = JWTManager.get_payload(token)
        if payload:
            self.id = payload.get("user_id")
            self.name = payload.get("user_name")
            self.role = payload.get("user_role")
            self.token = token
            self.payload = payload

    def user_exists(self):
        with DatabaseManager().session_scope() as session:
            try:
                collaborateur = session.query(Collaborateur).filter_by(
                    id=self.id).first()
                if not collaborateur:
                    return False
                return True
            except Exception as e:
                ErrorMessage.database_error()
                sentry_sdk.capture_exception(e)
                return False

    @staticmethod
    def create_account(db_manager: DatabaseManager):
        """
        Crée un compte collaborateur.
        """
        JWTManager.delete_token()
        WarningMessage.cancel_command_info()

        with db_manager.session_scope() as session:
            try:
                while True:
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
                        nom = f"{prenom.capitalize()} {nom_de_famille.upper()}"
                        break

                    collab = session.query(Collaborateur
                                           ).filter_by(nom=nom).first()
                    if collab:
                        ErrorMessage.collab_already_exists(nom)
                        continue
                    break

                # Rôle
                roles = session.query(Role).all()
                role_choices = [role.nom for role in roles]
                role_choices.append("Annuler")

                while True:
                    role_name = Utils.get_questionnary(role_choices)
                    if role_name == "Annuler":
                        WarningMessage.action_cancelled()
                        return

                    role = session.query(Role).filter_by(nom=role_name).first()

                    if not role:
                        ErrorMessage.data_not_found("Rôle", role_name)
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

                # Email
                email = f"{
                    slugify.slugify(prenom)}.{
                    slugify.slugify(nom_de_famille)}" + "@epicevents.com"
            except KeyboardInterrupt:
                WarningMessage.action_cancelled()
                return

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
