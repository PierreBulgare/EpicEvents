from models import Client, Collaborateur
from datetime import datetime
from utils.jwt_utils import JWTManager
from utils.utils import Utils
from messages_managers.text import TextManager
from messages_managers.error import ErrorMessage
from messages_managers.success import SuccessMessage
from messages_managers.warning import WarningMessage
from .database import DatabaseManager
from .user import UserManager
from utils.auth import AuthManager
from app.settings import QUIT_APP_CHOICES
from utils.permission import Permission


class ClientManager:
    def __init__(self, db_manager: DatabaseManager, user: UserManager):
        self.db_manager = db_manager
        self.user = user

    def display_client_data(self, client: Client):
        """
        Affiche les informations d'un client.
        Nom complet, email, téléphone et nom de l'entreprise.
        """
        Utils.new_screen(self.user)

        print(
            TextManager.style(
                TextManager.color("Informations du client".center(50), "blue"),
                "bold"
            )
        )
        print(TextManager.color(f"{'Champ':<20} {'Valeur':<30}", "yellow"))
        print("-" * 50)
        print(
            f"{'Nom complet':<20} "
            f"{TextManager.style(client.nom_complet, 'dim'):<30}"
        )
        print(f"{'Email':<20} {TextManager.style(client.email, 'dim'):<30}")
        print(
            f"{'Téléphone':<20} "
            f"{TextManager.style(client.telephone, 'dim'):<30}"
        )
        print(
            f"{'Nom de l\'entreprise':<20} "
            f"{TextManager.style(client.nom_entreprise, 'dim'):<30}"
        )
        print("-" * 50)

    @staticmethod
    def get_client(session, warning=False) -> Client:
        """
        Récupère un client à partir de son email.
        """
        if warning:
            WarningMessage.cancel_command_info()

        while True:
            try:
                client_email = input("Email du client : ").strip()
                if not client_email:
                    ErrorMessage.email_empty()
                    continue
                client = session.query(Client
                                       ).filter_by(email=client_email
                                                   ).first()
                if not client:
                    ErrorMessage.data_not_found(
                        "Client", client_email)
                    continue
                return client
            except KeyboardInterrupt:
                WarningMessage.action_cancelled()
                return

    def display_client(self, client_id=None, success_message=None):
        """
        Affiche les informations d'un client avec un menu d'actions.
        Actions : Modifier, Supprimer.
        """
        if not JWTManager.token_valid(self.user):
            return

        with self.db_manager.session_scope() as session:
            if not client_id:
                client = ClientManager.get_client(session)
                if not client:
                    return
            else:
                client = session.query(Client).filter_by(id=client_id).first()

            self.display_client_data(client)

            if not Permission.client_management(self.user.role):
                return

            if str(client.commercial.id) != str(self.user.id):
                return

            if success_message:
                success_message(client.nom_complet)

            choices = [
                "✏️  Modifier",
                "❌ Supprimer",
                "🔙 Retour"
            ] + QUIT_APP_CHOICES

            while True:
                action = Utils.get_questionnary(choices)

                match action:
                    case "✏️  Modifier":
                        self.update_client(client.id)
                        break
                    case "❌ Supprimer":
                        self.delete_client(client.id)
                        break
                    case "🔙 Retour":
                        break
                    case "🔒 Déconnexion":
                        AuthManager.logout()
                    case "❌ Quitter l'application":
                        Utils.quit_app()
                    case _:
                        ErrorMessage.action_not_recognized()

    def display_all_clients(self):
        """
        Affiche la liste de tous les clients dans un tableau.
        """
        Utils.new_screen(self.user)

        if not JWTManager.token_valid(self.user):
            return

        with self.db_manager.session_scope() as session:
            clients = session.query(Client
                                    ).order_by(Client.nom_complet.asc()).all()
            if not clients:
                WarningMessage.empty_table(Client.__tablename__)
                return

            width = 50
            print(
                TextManager.style(
                    TextManager.color(
                        "Liste des clients".center(width), "blue"
                    ),
                    "bold"
                )
            )
            print("-" * width)
            print(TextManager.color(f"{'Nom':20} | {'Email':30}", "yellow"))
            print("-" * width)
            for client in clients:
                print(
                    f"{TextManager.style(
                        client.nom_complet.ljust(20), 'dim'
                    )} | "
                    f"{TextManager.style(client.email.ljust(30), 'dim')}"
                )
            print("-" * width)

    def create_client(self):
        """
        Crée un nouveau client.
        Informations obligatoires : Nom complet, email.
        Informations facultatives : Téléphone, nom de l'entreprise.
        """
        if not JWTManager.token_valid(self.user):
            return

        if not Permission.client_management(self.user.role):
            return

        WarningMessage.cancel_command_info()

        while True:
            try:
                nom_complet = input("Nom complet : ").strip()
                if not nom_complet:
                    ErrorMessage.client_name_empty()
                    continue
                email = input("Email : ").strip()
                if not email:
                    ErrorMessage.email_empty()
                    continue
                if "@" not in email or "." not in email.split("@")[-1]:
                    ErrorMessage.invalid_email()
                    continue
                telephone = input("Téléphone (Facultatif) : ").strip()
                nom_entreprise = input(
                    "Nom de l'entreprise (Facultatif): "
                ).strip()
                break
            except KeyboardInterrupt:
                WarningMessage.action_cancelled()
                return

        with self.db_manager.session_scope() as session:
            client = Client(
                nom_complet=nom_complet,
                email=email,
                telephone=telephone,
                nom_entreprise=nom_entreprise,
                date_creation=datetime.now(),
                derniere_maj=datetime.now(),
                commercial=session.query(Collaborateur
                                         ).filter_by(id=self.user.id).first()
            )
            session.add(client)
            session.commit()
            self.display_client(client.id, SuccessMessage.create_success)

    def update_client(self, client_id=None):
        """
        Met à jour les informations d'un client existant.
        Champs modifiables :
        - Nom complet
        - Email
        - Téléphone
        - Nom de l'entreprise
        """
        if not JWTManager.token_valid(self.user):
            return

        if not Permission.client_management(self.user.role):
            return

        with self.db_manager.session_scope() as session:
            if not client_id:
                client = ClientManager.get_client(session)
                if not client:
                    return
            else:
                client = session.query(Client).filter_by(id=client_id).first()

            if str(client.commercial.id) != str(self.user.id):
                ErrorMessage.client_not_assigned_to_user(edit=True)
                return

            choices = [
                "Nom complet",
                "Email",
                "Téléphone",
                "Nom de l'entreprise",
                "Tout modifier",
                "Retour"
            ]

            message = None

            while True:
                self.display_client_data(client)
                if message:
                    message()
                    message = None
                action = Utils.get_questionnary(choices, edit=True)

                match action:
                    case "Nom complet":
                        message = self.update_nom_complet(session, client)
                    case "Email":
                        message = self.update_email(session, client)
                    case "Téléphone":
                        message = self.update_telephone(session, client)
                    case "Nom de l'entreprise":
                        message = self.update_nom_entreprise(session, client)
                    case "Tout modifier":
                        messages = [
                            self.update_nom_complet(session, client),
                            self.update_email(session, client),
                            self.update_telephone(session, client),
                            self.update_nom_entreprise(session, client)
                        ]
                        for msg in messages:
                            if msg:
                                message = msg
                                break
                    case "Retour":
                        break
                    case _:
                        ErrorMessage.action_not_recognized()
                        continue

    def update_nom_complet(self, session, client: Client) -> str:
        """
        Met à jour le nom complet d'un client.
        """
        message = None
        while True:
            nom_complet = Utils.get_input(
                "Nom complet :", client.nom_complet)
            if client.nom_complet != nom_complet:
                if not nom_complet:
                    ErrorMessage.client_name_empty()
                    continue
                client.nom_complet = nom_complet
                message = SuccessMessage.update_success
                self.db_manager.update_commit(client, session)
            return message

    def update_email(self, session, client: Client) -> str:
        """
        Met à jour l'email d'un client.
        """
        message = None
        while True:
            email = Utils.get_input(
                "Email :", client.email)
            if client.email != email:
                if not email:
                    ErrorMessage.email_empty()
                    continue
                if not Utils.email_is_valid(email):
                    ErrorMessage.invalid_email()
                    continue
                query = session.query(Client
                                      ).filter_by(email=email
                                                  ).first()
                if query:
                    ErrorMessage.client_email_already_exists(
                        email
                    )
                    continue
                client.email = email
                message = SuccessMessage.update_success
                self.db_manager.update_commit(client, session)
            return message

    def update_telephone(self, session, client: Client) -> str:
        """
        Met à jour le numéro de téléphone d'un client.
        """
        message = None
        telephone = Utils.get_input(
            "Téléphone (Facultatif) :", client.telephone)
        if client.telephone != telephone:
            client.telephone = telephone
            message = SuccessMessage.update_success
            self.db_manager.update_commit(client, session)
        return message

    def update_nom_entreprise(self, session, client: Client) -> str:
        """
        Met à jour le nom de l'entreprise d'un client.
        """
        message = None
        nom_entreprise = Utils.get_input(
            "Nom de l'entreprise (Facultatif) :",
            client.nom_entreprise
        )
        if client.nom_entreprise != nom_entreprise:
            client.nom_entreprise = nom_entreprise
            message = SuccessMessage.update_success
            self.db_manager.update_commit(client, session)
        return message

    def delete_client(self, client_id=None):
        """
        Supprime un client de la base de données.
        """
        if not JWTManager.token_valid(self.user):
            return

        if not Permission.client_management(self.user.role):
            return

        with self.db_manager.session_scope() as session:
            if not client_id:
                client = ClientManager.get_client(session, warning=True)
                if not client:
                    return
            else:
                client = session.query(Client).filter_by(id=client_id).first()

            if str(client.commercial.id) != str(self.user.id):
                ErrorMessage.client_not_assigned_to_user(delete=True)
                return

            if not Utils.confirm_deletion():
                return

            session.delete(client)
            session.commit()
            Utils.new_screen(self.user)
            SuccessMessage.delete_success()
