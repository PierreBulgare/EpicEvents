import questionary
from .jwt_utils import JWTManager
from .utils import Utils
from .auth import AuthManager
from app.settings import QUIT_APP_CHOICES
from models_managers.database import DatabaseManager
from models_managers.client import ClientManager
from models_managers.contract import ContractManager
from models_managers.event import EventManager
from models_managers.role import RoleManager
from messages_managers.error import ErrorMessage


class MenuManager:
    def __init__(self, db_manager: DatabaseManager, user=None):
        self.user = user
        self.db_manager = db_manager
        self.client_manager = ClientManager(db_manager, user)
        self.contract_manager = ContractManager(db_manager, user)
        self.event_manager = EventManager(db_manager, user)

    def main_page(self):
        Utils.new_screen(self.user)

        choices = [
            "🔑 Se connecter",
            "📝 Créer un compte",
            "❌ Quitter l'application"
            ]

        if not JWTManager.token_exist():
            while True:
                action = questionary.select(
                    "🔑 Connexion/Inscription",
                    choices=choices,
                    use_shortcuts=True,
                    instruction=" ",
                ).ask()

                match action:
                    case "🔑 Se connecter":
                        AuthManager.login(self.db_manager)
                        token = JWTManager.get_token()
                        payload = JWTManager.get_payload(token)
                        if payload:
                            self.user.init_user(token, payload)
                            break
                    case "📝 Créer un compte":
                        self.user.create_account(self.db_manager)
                        continue
                    case "❌ Quitter l'application":
                        Utils.quit_app()
                    case _:
                        ErrorMessage.action_not_recognized()
        else:
            token = JWTManager.get_token()
            payload = JWTManager.get_payload(token)
            if payload is None:
                ErrorMessage.invalid_token()
                AuthManager.login()
                token = JWTManager.get_token()
                payload = JWTManager.get_payload(token)
                if payload:
                    self.user.init_user(token, payload)
            else:
                self.user.init_user(token, payload)


    def main_menu(self):
        Utils.new_screen(self.user)
        
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
                    Utils.quit_app()
                case "🔒 Quitter l'application (Avec Déconnexion)":
                    Utils.quit_app(user_logout=True)
                case _:
                    ErrorMessage.action_not_recognized()

    def manage_clients(self):
        Utils.new_screen(self.user)

        CHOICES = [
            "👤 Afficher tous les clients",
            "👤 Afficher un client",
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
                case "👤 Afficher un client":
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
                    Utils.quit_app()
                case "🔒 Quitter l'application (Avec Déconnexion)":
                    Utils.quit_app(user_logout=True)
                case _:
                    ErrorMessage.action_not_recognized()

    def manage_contract(self):
        Utils.new_screen(self.user)

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
                    Utils.quit_app()
                case "🔒 Quitter l'application (Avec Déconnexion)":
                    Utils.quit_app(user_logout=True)
                case _:
                    ErrorMessage.action_not_recognized()


    def manage_events(self):
        Utils.new_screen(self.user)

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
                    Utils.quit_app()
                case "🔒 Quitter l'application (Avec Déconnexion)":
                    Utils.quit_app(user_logout=True)
                case _:
                    ErrorMessage.action_not_recognized()


    def admin_menu(self):
        """
        Menu d'administration

        Actions disponibles:
            - Créer ou mettre à jour les tables
            - Créer les rôles
            - Supprimer les tables
        """
        Utils.new_screen(self.user, admin=True)

        CHOICES = [
            "Créer ou mettre à jour les tables",
            "Créer un rôle",
            "Supprimer les tables",
            "Quitter l'application"
        ]

        while True:
            action = questionary.select(
                "Que voulez-vous faire ?",
                choices=CHOICES,
                use_shortcuts=True,
                instruction=" ",
            ).ask()

            match action:
                case "Créer ou mettre à jour les tables":
                    self.db_manager.create_all()
                case "Créer un rôle":
                    RoleManager.create_role(self.db_manager)
                case "Supprimer les tables":
                    self.db_manager.drop_all()
                case "Quitter l'application":
                    Utils.quit_app()
                case _:
                    ErrorMessage.action_not_recognized()
