from models import Collaborateur, Role
from messages_managers.error import ErrorMessage
from messages_managers.warning import WarningMessage
from messages_managers.success import SuccessMessage
from messages_managers.text import TextManager
from .database import DatabaseManager
from .user import UserManager
from utils.utils import Utils
from utils.jwt_utils import JWTManager
from utils.permission import Permission
from utils.auth import AuthManager
from utils.password_security import PasswordSecurity
from app.settings import QUIT_APP_CHOICES
import slugify


class CollaborateurManager:
    def __init__(self, db_manager: DatabaseManager, user: UserManager):
        self.db_manager = db_manager
        self.user = user

    def display_collab_data(self, collab: Collaborateur):
        Utils.new_screen(self.user)

        width = 50
        print(
            TextManager.style(
                TextManager.color(
                    "Informations du collaborateur".center(width), "blue"
                ),
                "bold"
            )
        )
        print("-" * width)
        print(
            f"{'Nom':<20} "
            f"{TextManager.style(collab.nom, 'dim'):<30}"
        )
        print(
            f"{'Email':<20} "
            f"{TextManager.style(collab.email, 'dim'):<30}"
        )
        print(
            f"{'Département':<20} "
            f"{TextManager.style(collab.role, 'dim'):<30}"
        )
        print("-" * width)

    @staticmethod
    def get_collaborateur(session, warning=False):
        if warning:
            WarningMessage.cancel_command_info()

        while True:
            try:
                email = input("Email du collaborateur : ")
                if not email:
                    ErrorMessage.client_name_empty()
                    continue
                if not Utils.email_is_valid(email):
                    ErrorMessage.invalid_email()
                    continue
                collab = session.query(Collaborateur
                                       ).filter_by(email=email
                                                   ).first()
                if not collab:
                    ErrorMessage.data_not_found("Collaborateur", email)
                    continue
                return collab
            except KeyboardInterrupt:
                WarningMessage.action_cancelled()
                return

    def display_collab(self, collab_id=None, success_message=None):
        if not JWTManager.token_valid(self.user):
            return

        if not Permission.collab_management(self.user.role):
            return

        with self.db_manager.session_scope() as session:
            if not collab_id:
                collab = self.get_collaborateur(session, warning=True)
                if not collab:
                    return
            else:
                collab = session.query(Collaborateur
                                       ).filter_by(id=collab_id).first()

            self.display_collab_data(collab)

            if success_message:
                success_message()

            choices = [
                "✏️  Modifier",
                "❌ Supprimer",
                "🔙 Retour"
            ] + QUIT_APP_CHOICES

            while True:
                action = Utils.get_questionnary(choices)

                match action:
                    case "✏️  Modifier":
                        self.update_collab(collab.id)
                        break
                    case "❌ Supprimer":
                        self.delete_collab(collab.id)
                        break
                    case "🔙 Retour":
                        break
                    case "🔒 Déconnexion":
                        AuthManager.logout()
                    case "❌ Quitter l'application":
                        Utils.quit_app()
                    case _:
                        ErrorMessage.action_not_recognized()

    def create_collab(self):
        if not JWTManager.token_valid(self.user):
            return

        if not Permission.collab_management(self.user.role):
            return

        WarningMessage.cancel_command_info()

        with self.db_manager.session_scope() as session:
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

                # Email
                email = f"{
                    slugify.slugify(prenom)}.{
                    slugify.slugify(nom_de_famille)}" + "@epicevents.com"

                # Mot de passe
                password = Utils.generate_password()
                # Sauvegarde du mot de passe généré dans un fichier
                # fake-passwords
                with open(f"./fake-passwords/{email}.txt", "a") as file:
                    file.write(password)
            except KeyboardInterrupt:
                WarningMessage.action_cancelled()
                return

            # Création du collaborateur
            new_collab = Collaborateur(
                nom=nom,
                email=email,
                password_hash=PasswordSecurity.hash(password),
                role=role,
            )

            session.add(new_collab)
            session.commit()

            SuccessMessage.collab_created(new_collab.nom)

    def delete_collab(self, collab_id=None):
        if not JWTManager.token_valid(self.user):
            return

        if not Permission.collab_management(self.user.role):
            return

        with self.db_manager.session_scope() as session:
            if not collab_id:
                collab = self.get_collaborateur(session, warning=True)
                if not collab:
                    return
            else:
                collab = session.query(Collaborateur
                                       ).filter_by(id=collab_id).first()

            if not Utils.confirm_deletion():
                return

            session.delete(collab)
            session.commit()
            Utils.new_screen(self.user)
            SuccessMessage.delete_success()
