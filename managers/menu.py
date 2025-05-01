import sys
import utils
import questionary
from jwt_utils import get_payload, get_token, token_exist
from auth import login, create_account, logout
from settings import QUIT_APP_CHOICES
from .message import MessageManager
from .role import RoleManager
from .client import ClientManager
from .contract import ContractManager
from .event import EventManager
from .user import UserManager


class MenuManager:
    def __init__(self, db_manager, user:UserManager=None):
        self.user = user
        self.db_manager = db_manager
        self.client_manager = ClientManager(db_manager, user)
        self.contract_manager = ContractManager(db_manager, user)
        self.event_manager = EventManager(db_manager, user)

    def main_page(self):
        utils.new_screen(self.user)

        choices = [
            "🔑 Se connecter",
            "📝 Créer un compte",
            "❌ Quitter l'application"
            ]

        if not token_exist():
            while True:
                action = questionary.select(
                    "🔑 Connexion/Inscription",
                    choices=choices,
                    use_shortcuts=True,
                    instruction=" ",
                ).ask()

                match action:
                    case "🔑 Se connecter":
                        login()
                        token = get_token()
                        payload = get_payload(token)
                        if payload:
                            self.user.init_user(token, payload)
                            break
                        else:
                            MessageManager.invalid_token()
                            continue
                    case "📝 Créer un compte":
                        create_account()
                        continue
                    case "❌ Quitter l'application":
                        utils.quit_app()
                    case _:
                        MessageManager.action_not_recognized()
        else:
            token = get_token()
            payload = get_payload(token)
            if payload is None:
                MessageManager.invalid_token()
                login()
                token = get_token()
                payload = get_payload(token)
                if payload:
                    self.user.init_user(token, payload)
            else:
                self.user.init_user(token, payload)


    def main_menu(self):
        utils.new_screen(self.user)
        
        choices = QUIT_APP_CHOICES.copy()
        if self.user.role == "Commercial":
            choices.insert(0, "👤 Gérer les clients")
            choices.insert(1, "🎫 Gérer les événements")
        elif self.user.role == "Gestion":
            choices.insert(0, "📜 Gérer les contrats")
            choices.insert(1, "🎫 Gérer les événements")
        elif self.user.role == "Support":
            choices.insert(0, "🎫 Gérer les événements")
        while True:
            action = questionary.select(
                "📑 Menu Principal",
                choices=choices,
                use_shortcuts=True,
                instruction=" ",
            ).ask()

            match action:
                case "👤 Gérer les clients":
                    self.manage_clients()
                    continue
                case "📜 Gérer les contrats":
                    self.manage_contract()
                    continue
                case "🎫 Gérer les événements":
                    self.manage_events()
                    continue
                case "❌ Quitter l'application (Sans Déconnexion)":
                    utils.quit_app()
                case "🔒 Quitter l'application (Avec Déconnexion)":
                    utils.quit_app(user_logout=True)
                case _:
                    MessageManager.action_not_recognized()

    def manage_clients(self):
        utils.new_screen(self.user)

        CHOICES = [
            "👤 Afficher tous les clients",
            "👤 Afficher les informations d'un client",
            "🆕 Ajouter un client",
            "✏️  Modifier un client",
            "❌ Supprimer un client",
            "🔙 Retourner au menu principal"
        ] + QUIT_APP_CHOICES

        while True:
            action = questionary.select(
                "Menu Principal",
                choices=CHOICES,
                use_shortcuts=True,
                instruction=" "
            ).ask()

            match action:
                case "👤 Afficher tous les clients":
                    self.client_manager.display_all_clients()
                    continue
                case "👤 Afficher les informations d'un client":
                    self.client_manager.display_client()
                    continue
                case "🆕 Ajouter un client":
                    self.client_manager.create_client()
                    continue
                case "✏️  Modifier un client":
                    self.client_manager.update_client()
                    continue
                case "❌ Supprimer un client":
                    self.client_manager.delete_client()
                    continue
                case "🔙 Retourner au menu principal":
                    break
                case "❌ Quitter l'application (Sans Déconnexion)":
                    utils.quit_app()
                case "🔒 Quitter l'application (Avec Déconnexion)":
                    utils.quit_app(user_logout=True)
                case _:
                    MessageManager.action_not_recognized()

    def manage_contract(self):
        utils.new_screen(self.user)

        CHOICES = [
            "🗂️  Afficher tous les contrats",
            "📜 Afficher un contrat",
            "🆕 Créer un contrat",
            "✏️  Modifier un contrat",
            "🖋️  Signer un contrat",
            "❌ Supprimer un contrat",
            "🔙 Retourner au menu principal"
        ] + QUIT_APP_CHOICES

        while True:
            action = questionary.select(
                "Menu Principal",
                choices=CHOICES,
                use_shortcuts=True,
                instruction=" ",
            ).ask()

            match action:
                case "🗂️  Afficher tous les contrats":
                    self.contract_manager.display_all_contracts()
                    continue
                case "📜 Afficher un contrat":
                    self.contract_manager.display_contract()
                    continue
                case "🆕 Créer un contrat":
                    self.contract_manager.create_contract()
                    continue
                case "✏️  Modifier un contrat":
                    self.contract_manager.update_contract()
                    continue
                case "🖋️  Signer un contrat":
                    self.contract_manager.sign_contract()
                    continue
                case "❌ Supprimer un contrat":
                    self.contract_manager.delete_contract()
                    continue
                case "🔙 Retourner au menu principal":
                    break
                case "❌ Quitter l'application (Sans Déconnexion)":
                    utils.quit_app()
                case "🔒 Quitter l'application (Avec Déconnexion)":
                    utils.quit_app(user_logout=True)
                case _:
                    MessageManager.action_not_recognized()


    def manage_events(self):
        utils.new_screen(self.user)

        CHOICES = [
            "🗂️  Afficher tous les événements",
            "🎫 Afficher un événement",
            "🆕 Créer un événement",
            "✏️  Modifier un événement",
            "❌ Supprimer un événement",
            "🔙 Retourner au menu principal"
        ] + QUIT_APP_CHOICES

        while True:
            action = questionary.select(
                "Menu Principal",
                choices=CHOICES,
                use_shortcuts=True,
                instruction=" ",
            ).ask()

            match action:
                case "🗂️  Afficher tous les événements":
                    self.event_manager.display_all_events()
                    continue
                case "🎫 Afficher un événement":
                    self.event_manager.display_event()
                    continue
                case "🆕 Créer un événement":
                    self.event_manager.create_event()
                    continue
                case "✏️  Modifier un événement":
                    self.event_manager.update_event()
                    continue
                case "❌ Supprimer un événement":
                    self.event_manager.delete_event()
                    continue
                case "🔙 Retourner au menu principal":
                    break
                case "❌ Quitter l'application (Sans Déconnexion)":
                    utils.quit_app()
                case "🔒 Quitter l'application (Avec Déconnexion)":
                    utils.quit_app(user_logout=True)
                case _:
                    MessageManager.action_not_recognized()


    def admin_menu(self):
        utils.new_screen(self.user, admin=True)

        role_manager = RoleManager(self.db_manager, self.user)
        while True:
            action = questionary.select(
                "Que voulez-vous faire ?",
                choices=[
                    "Créer ou mettre à jour les tables",
                    "Créer un rôle",
                    "Supprimer les tables",
                    "Quitter l'application"
                ],
                use_shortcuts=True,
                instruction=" ",
            ).ask()

            match action:
                case "Créer ou mettre à jour les tables":
                    self.db_manager.create_all()
                case "Créer un rôle":
                    role_manager.create_role()
                case "Supprimer les tables":
                    self.db_manager.drop_all()
                case "Quitter l'application":
                    print("Merci d'avoir utilisé l'application EPIC Events !")
                    exit(0)
                case _:
                    print("Action non reconnue. Veuillez réessayer.")