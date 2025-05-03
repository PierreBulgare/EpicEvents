from models import Client, Collaborateur
from datetime import datetime
from utils.jwt_utils import JWTManager
from utils.utils import Utils
import questionary
from messages_managers.text import TextManager
from messages_managers.error import ErrorMessage
from messages_managers.success import SuccessMessage
from messages_managers.warning import WarningMessage
from .database import DatabaseManager
from .user import UserManager
from app.settings import QUIT_APP_CHOICES


class ClientManager:
    def __init__(self, db_manager: DatabaseManager, user: UserManager):
        self.db_manager = db_manager
        self.user = user

    def display_client_data(self, client: Client):
        Utils.new_screen(self.user)
        print(TextManager.style(TextManager.color("Informations du client".center(50), "blue"), "bold"))
        print(TextManager.color(f"{'Champ':<20} {'Valeur':<30}", "yellow"))
        print("-" * 50)
        print(f"{'Nom complet':<20} {TextManager.style(client.nom_complet, 'dim'):<30}")
        print(f"{'Email':<20} {TextManager.style(client.email, 'dim'):<30}")
        print(f"{'Téléphone':<20} {TextManager.style(client.telephone, 'dim'):<30}")
        print(f"{'Nom de l\'entreprise':<20} {TextManager.style(client.nom_entreprise, 'dim'):<30}")
        print("-" * 50)

    def display_client(self, client_id = None, success_message = None):
        if not JWTManager.token_valid(self.user):
            return
        
        
        with self.db_manager.session_scope() as session:
            if not client_id:
                try:
                    WarningMessage.cancel_command_info()
                    client_email = input("Email du client à afficher : ").strip()
                    if not client_email:
                        ErrorMessage.email_empty()
                        return
                    client = session.query(Client).filter_by(email=client_email).first()
                    if not client:
                        ErrorMessage.data_not_found("Client", client_email)
                        return
                except KeyboardInterrupt:
                    WarningMessage.action_cancelled()
                    return
            else:
                client = session.query(Client).filter_by(id=client_id).first()
            
            self.display_client_data(client)

            if success_message:
                success_message(client.nom_complet)
            
            CHOICES = [
                "✏️  Modifier",
                "❌ Supprimer",
                "🔙 Retour"
            ] + QUIT_APP_CHOICES
            while True:
                action = questionary.select(
                    "Que voulez-vous faire ?",
                    choices=CHOICES,
                    use_shortcuts=True,
                    instruction=" ",
                ).ask()

                match action:
                    case "✏️  Modifier":
                        self.update_client(client.id)
                        break
                    case "❌ Supprimer":
                        self.delete_client(client.id)
                        break
                    case "🔙 Retour":
                        break
                    case "❌ Quitter l'application (Sans Déconnexion)":
                        Utils.quit_app()
                    case "🔒 Quitter l'application (Avec Déconnexion)":
                        Utils.quit_app(user_logout=True)
                    case _:
                        ErrorMessage.action_not_recognized()

    def display_all_clients(self):
        Utils.new_screen(self.user)
        if not JWTManager.token_valid(self.user):
            return
        
        with self.db_manager.session_scope() as session:
            clients = session.query(Client).all()
            if not clients:
                WarningMessage.empty_table(Client.__tablename__)
                return
            
            width = 50
            print(TextManager.style(TextManager.color("Liste des clients".center(width), "blue"), "bold"))
            print("-" * width)
            print(TextManager.color(f"{'Nom':20} | {'Email':30}", "yellow"))
            print("-" * width)
            for client in clients:
                print(f"{TextManager.style(client.nom_complet.ljust(20), 'dim')} | {TextManager.style(client.email.ljust(30), 'dim')}")
            print("-" * width)


    def create_client(self):
        WarningMessage.cancel_command_info()

        if not JWTManager.token_valid(self.user):
            return
        
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
                nom_entreprise = input("Nom de l'entreprise (Facultatif): ").strip()
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
                commercial=session.query(Collaborateur).filter_by(id=self.user.id).first()
            )
            session.add(client)
            session.commit()
            self.display_client(client.id, SuccessMessage.create_success)

    def update_client(self, client_id = None):
        if not JWTManager.token_valid(self.user):
            return

        with self.db_manager.session_scope() as session:
            WarningMessage.cancel_command_info()
            if not client_id:
                while True:
                    try:
                        client_email = input("Email du client à modifier : ").strip()
                        if not client_email:
                            ErrorMessage.email_empty()
                            continue
                        client = session.query(Client).filter_by(email=client_email).first()
                        if not client:
                            ErrorMessage.data_not_found("Client", client_email)
                            continue
                        self.display_client_data(client)
                    except KeyboardInterrupt:
                        WarningMessage.action_cancelled()
                        return
            else:
                client = session.query(Client).filter_by(id=client_id).first()
                
            CHOICES = [
                "Nom complet",
                "Email",
                "Téléphone",
                "Nom de l'entreprise",
                "Tout modifier",
                "Retour"
            ]

            while True:
                action = questionary.select(
                    "Que voulez-vous modifier ?",
                    choices=CHOICES,
                    use_shortcuts=True,
                    instruction=" ",
                ).ask()

                match action:
                    case "Nom complet":
                        while True:
                            nom_complet = questionary.text(
                                f"Nom complet : ",
                                default=client.nom_complet
                            ).ask()
                            if not nom_complet:
                                ErrorMessage.client_name_empty()
                                continue
                            break
                        client.nom_complet = nom_complet
                    case "Email":
                        while True:
                            email = questionary.text(
                                f"Email : ",
                                default=client.email
                            ).ask()
                            if not email:
                                ErrorMessage.email_empty()
                                continue
                            if "@" not in email or "." not in email.split("@")[-1]:
                                ErrorMessage.invalid_email()
                                continue
                            break
                        client.email = email
                    case "Téléphone":
                        telephone = questionary.text(
                            f"Téléphone (Facultatif) : ",
                            default=client.telephone
                        ).ask()
                        client.telephone = telephone
                        break
                    case "Nom de l'entreprise":
                        nom_entreprise = questionary.text(
                            f"Nom de l'entreprise (Facultatif) : ",
                            default=client.nom_entreprise
                        ).ask()
                        client.nom_entreprise = nom_entreprise
                        break
                    case "Tout modifier":
                        while True:
                            nom_complet = questionary.text(
                                f"Nom complet : ",
                                default=client.nom_complet
                            ).ask()
                            if not nom_complet:
                                ErrorMessage.client_name_empty()
                                continue
                            break
                        while True:
                            email = questionary.text(
                                f"Email : ",
                                default=client.email
                            ).ask()
                            if not email:
                                ErrorMessage.email_empty()
                                continue
                            if "@" not in email or "." not in email.split("@")[-1]:
                                ErrorMessage.invalid_email()
                                continue
                            break
                        telephone = questionary.text(
                            "Téléphone (Facultatif) : ",
                            default=client.telephone
                        ).ask()
                        nom_entreprise = questionary.text(
                            "Nom de l'entreprise (Facultatif) : ",
                            default=client.nom_entreprise
                        ).ask()
                        break
                    case "Retour":
                        break
                    case _:
                        ErrorMessage.action_not_recognized()

            client.derniere_maj = datetime.now()
            
            session.commit()
            self.display_client(client.id, SuccessMessage.update_success)

    def delete_client(self, client_id = None):
        if not JWTManager.token_valid(self.user):
            return
            
        with self.db_manager.session_scope() as session:
            WarningMessage.cancel_command_info()
            if not client_id:
                while True:
                    try:
                        client_email = input("Email du client à supprimer : ").strip()
                        if not client_email:
                            ErrorMessage.email_empty()
                            continue
                        client = session.query(Client).filter_by(email=client_email).first()
                        if not client:
                            ErrorMessage.data_not_found("Client", client_email)
                            continue
                        self.display_client_data(client)
                    except KeyboardInterrupt:
                        WarningMessage.action_cancelled()
                        return
            else:
                client = session.query(Client).filter_by(id=client_id).first()
            

            while True:
                confirmation = questionary.select(
                    f"Êtes-vous sûr de vouloir supprimer le client '{client.nom_complet}' ?",
                    choices=["Oui", "Non"],
                    use_shortcuts=True,
                    instruction=" ",
                ).ask()

                match confirmation:
                    case "Oui":
                        break
                    case "Non":
                        WarningMessage.action_cancelled()
                        return
                    case _:
                        ErrorMessage.action_not_recognized()
            
            # Suppression du client
            session.delete(client)
            session.commit()
            Utils.new_screen(self.user)
            SuccessMessage.delete_success()
