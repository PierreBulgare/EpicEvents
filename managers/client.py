from models import Client, Collaborateur
from datetime import datetime
from jwt_utils import token_valid
import uuid
import questionary
from .text import TextManager
from .message import MessageManager
from .database import DatabaseManager
from .user import UserManager
import utils
from settings import QUIT_APP_CHOICES

class ClientManager:
    def __init__(self, db_manager: DatabaseManager, user: UserManager):
        self.db_manager = db_manager
        self.user = user

    def display_client_data(self, client: Client):
        print(TextManager.style(TextManager.color("Informations du client".center(50), "blue"), "bold"))
        print(TextManager.color(f"{'Champ':<20} {'Valeur':<30}", "yellow"))
        print("-" * 50)
        print(f"{'Nom complet':<20} {TextManager.style(client.nom_complet, 'dim'):<30}")
        print(f"{'Email':<20} {TextManager.style(client.email, 'dim'):<30}")
        print(f"{'Téléphone':<20} {TextManager.style(client.telephone, 'dim'):<30}")
        print(f"{'Nom de l\'entreprise':<20} {TextManager.style(client.nom_entreprise, 'dim'):<30}")
        print("-" * 50)

    def display_client(self):
        if not token_valid(self.user):
            return
        
        client_email = input("Email du client à afficher : ")
        with self.db_manager.session_scope() as session:
            client = session.query(Client).filter_by(email=client_email).first()
            if not client:
                MessageManager.data_not_found("Client", client_email)
                return
            
            self.display_client_data(client)
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
                        self.update_client(client)
                        break
                    case "❌ Supprimer":
                        self.delete_client(client)
                        break
                    case "🔙 Retour":
                        break
                    case "❌ Quitter l'application (Sans Déconnexion)":
                        utils.quit_app()
                    case "🔒 Quitter l'application (Avec Déconnexion)":
                        utils.quit_app(user_logout=True)
                    case _:
                        MessageManager.action_not_recognized()

    def display_all_clients(self):
        if not token_valid(self.user):
            return
        
        with self.db_manager.session_scope() as session:
            clients = session.query(Client).all()
            if not clients:
                MessageManager.empty_table(Client.__tablename__)
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
        MessageManager.cancel_command_info()

        if not token_valid(self.user):
            return
        try:
            nom_complet = input("Nom complet : ")
            email = input("Email : ")
            telephone = input("Téléphone : ")
            nom_entreprise = input("Nom de l'entreprise : ")
        except KeyboardInterrupt:
            MessageManager.action_cancelled()
            return

        with self.db_manager.session_scope() as session:
            client = Client(
                nom_complet=nom_complet,
                email=email,
                telephone=telephone,
                nom_entreprise=nom_entreprise,
                date_creation=datetime.now(),
                derniere_maj=datetime.now(),
                commercial=session.query(Collaborateur).filter_by(id=uuid.UUID(self.user.id)).first()
            )
            session.add(client)
            session.commit()
            MessageManager.create_success()

    def update_client(self, client: Client = None):
        if not token_valid(self.user):
            return

        with self.db_manager.session_scope() as session:
            if not client:
                try:
                    MessageManager.cancel_command_info()
                    client_email = input("Email du client à modifier : ")
                    client = session.query(Client).filter_by(email=client_email).first()
                    if not client:
                        MessageManager.data_not_found("Client", client_email)
                        return
                    self.display_client_data(client)
                except KeyboardInterrupt:
                    MessageManager.action_cancelled()
                    return
            else:
                client = session.merge(client)
                
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
                        nom_complet = questionary.text(
                            f"Nom complet :",
                            default=client.nom_complet
                        ).ask()
                        client.nom_complet = nom_complet
                        break
                    case "Email":
                        email = questionary.text(
                            f"Email :",
                            default=client.email
                        ).ask()
                        client.email = email
                        break
                    case "Téléphone":
                        telephone = questionary.text(
                            f"Téléphone :",
                            default=client.telephone
                        ).ask()
                        client.telephone = telephone
                        break
                    case "Nom de l'entreprise":
                        nom_entreprise = questionary.text(
                            f"Nom de l'entreprise :",
                            default=client.nom_entreprise
                        ).ask()
                        client.nom_entreprise = nom_entreprise
                        break
                    case "Tout modifier":
                        nom_complet = questionary.text(
                            "Nom complet :",
                            default=client.nom_complet
                        ).ask()
                        email = questionary.text(
                            "Email :",
                            default=client.email
                        ).ask()
                        telephone = questionary.text(
                            "Téléphone :",
                            default=client.telephone
                        ).ask()
                        nom_entreprise = questionary.text(
                            "Nom de l'entreprise :",
                            default=client.nom_entreprise
                        ).ask()
                        break
                    case "Retour":
                        break
                    case _:
                        MessageManager.action_not_recognized()


            client.derniere_maj = datetime.now()
            
            session.commit()
            MessageManager.update_success()

    def delete_client(self, client: Client = None):
        if not token_valid(self.user):
            return
            
        with self.db_manager.session_scope() as session:
            if not client:
                try:
                    MessageManager.cancel_command_info()
                    client_email = input("Email du client à supprimer : ")
                    client = session.query(Client).filter_by(email=client_email).first()
                    if not client:
                        MessageManager.data_not_found("Client", client_email)
                        return
                    self.display_client_data(client)
                except KeyboardInterrupt:
                    MessageManager.action_cancelled()
                    return
            else:
                client = session.merge(client)
            

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
                        MessageManager.action_cancelled()
                        return
                    case _:
                        MessageManager.action_not_recognized()
            
            # Suppression du client
            session.delete(client)
            session.commit()
            MessageManager.delete_success()