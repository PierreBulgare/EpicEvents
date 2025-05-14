from .jwt_utils import JWTManager
from .utils import Utils
from .auth import AuthManager
from app.settings import QUIT_APP_CHOICES, BACK_TO_MAIN_MENU
from models_managers.database import DatabaseManager
from models_managers.client import ClientManager
from models_managers.contract import ContractManager
from models_managers.event import EventManager
from models_managers.role import RoleManager
from models_managers.user import UserManager
from models_managers.collab import CollaborateurManager
from messages_managers.error import ErrorMessage
from .permission import Permission


class MenuManager:
    def __init__(self, db_manager: DatabaseManager, user: UserManager = None):
        self.user = user
        self.db_manager = db_manager
        self.collab_manager = CollaborateurManager(db_manager, user)
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
                action = Utils.get_questionnary(choices)

                match action:
                    case "🔑 Se connecter":
                        AuthManager.login(self.db_manager)
                        self.user.init_user()
                        if hasattr(self.user, "payload"):
                            break
                    case "📝 Créer un compte":
                        self.user.create_account(self.db_manager)
                        continue
                    case "❌ Quitter l'application":
                        Utils.quit_app()
                    case _:
                        ErrorMessage.action_not_recognized()
        else:
            payload = JWTManager.get_payload(JWTManager.get_token())
            if payload is None:
                ErrorMessage.invalid_token()
                AuthManager.login(self.db_manager)
                self.user.init_user()
            else:
                self.user.init_user()

            if not self.user.user_exists():
                JWTManager.delete_token()
                return

    def main_menu(self):
        choices = [
            "👤 Clients",
            "📜 Contrats",
            "🎫 Événements"
        ] + QUIT_APP_CHOICES

        if Permission.collab_management(self.user.role):
            choices.insert(0, "👤 Collaborateurs")

        while True:
            if not JWTManager.token_exist():
                break

            Utils.new_screen(self.user)
            Utils.display_menu_title("Menu principal")
            action = Utils.get_questionnary(choices)

            match action:
                case "👤 Collaborateurs":
                    self.manage_collabs()
                    continue
                case "👤 Clients":
                    self.manage_clients()
                    continue
                case "📜 Contrats":
                    self.manage_contract()
                    continue
                case "🎫 Événements":
                    self.manage_events()
                    continue
                case "🔒 Déconnexion":
                    AuthManager.logout()
                    break
                case "❌ Quitter l'application":
                    Utils.quit_app()
                case _:
                    ErrorMessage.action_not_recognized()

    def manage_collabs(self):
        Utils.new_screen(self.user)

        if not Permission.collab_management(self.user.role):
            return

        choices = [
            "👤 Afficher la liste des collaborateurs",
            "👤 Afficher un collaborateur",
            "🆕 Ajouter un collaborateur",
            "✏️  Modifier un collaborateur",
            "❌ Supprimer un collaborateur"
        ] + [BACK_TO_MAIN_MENU] + QUIT_APP_CHOICES

        while True:
            Utils.display_menu_title("Menu Collaborateur")
            action = Utils.get_questionnary(choices)

            match action:
                case "👤 Afficher la liste des collaborateurs":
                    self.collab_manager.display_all_collabs()
                    continue
                case "👤 Afficher un collaborateur":
                    self.collab_manager.display_collab()
                    continue
                case "🆕 Ajouter un collaborateur":
                    self.collab_manager.create_collab()
                    continue
                case "✏️  Modifier un collaborateur":
                    self.collab_manager.update_collab()
                    continue
                case "❌ Supprimer un collaborateur":
                    self.collab_manager.delete_collab()
                    continue
                case "🔙 Retour au menu principal":
                    break
                case "🔒 Déconnexion":
                    AuthManager.logout()
                    break
                case "❌ Quitter l'application":
                    Utils.quit_app()
                case _:
                    ErrorMessage.action_not_recognized()

    def manage_clients(self):
        Utils.new_screen(self.user)

        choices = [
            "👤 Afficher la liste des clients",
            "👤 Afficher un client"
        ]

        if Permission.client_management(self.user.role):
            choices.append("🆕 Ajouter un client")
            choices.append("✏️  Modifier un client")
            choices.append("❌ Supprimer un client")

        choices.extend([BACK_TO_MAIN_MENU] + QUIT_APP_CHOICES)

        while True:
            Utils.display_menu_title("Menu Client")
            action = Utils.get_questionnary(choices)

            match action:
                case "👤 Afficher la liste des clients":
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
                case "🔙 Retour au menu principal":
                    break
                case "🔒 Déconnexion":
                    AuthManager.logout()
                    break
                case "❌ Quitter l'application":
                    Utils.quit_app()
                case _:
                    ErrorMessage.action_not_recognized()

    def manage_contract(self):
        Utils.new_screen(self.user)

        choices = [
            "🗂️  Afficher la liste des contrats",
            "📜 Afficher un contrat"
        ]

        if Permission.contract_management(self.user.role):
            choices.append("🆕 Créer un contrat")
            choices.append("🖋️  Signer un contrat")
            choices.append("✏️  Modifier un contrat")
            choices.append("❌ Supprimer un contrat")

        choices.extend([BACK_TO_MAIN_MENU] + QUIT_APP_CHOICES)

        while True:
            Utils.display_menu_title("Menu Contrat")
            action = Utils.get_questionnary(choices)

            match action:
                case "🗂️  Afficher la liste des contrats":
                    self.contract_manager.display_all_contracts_menu()
                    continue
                case "📜 Afficher un contrat":
                    self.contract_manager.display_contract()
                    continue
                case "🆕 Créer un contrat":
                    self.contract_manager.create_contract()
                    continue
                case "🖋️  Signer un contrat":
                    self.contract_manager.sign_contract()
                    continue
                case "✏️  Modifier un contrat":
                    self.contract_manager.update_contract()
                    continue
                case "❌ Supprimer un contrat":
                    self.contract_manager.delete_contract()
                    continue
                case "🔙 Retour au menu principal":
                    break
                case "🔒 Déconnexion":
                    AuthManager.logout()
                    break
                case "❌ Quitter l'application":
                    Utils.quit_app()
                case _:
                    ErrorMessage.action_not_recognized()

    def manage_events(self):
        Utils.new_screen(self.user)

        choices = [
            "🗂️  Afficher la liste des événements",
            "🎫 Afficher un événement"
        ]

        if Permission.create_event(self.user.role):
            choices.append("🆕 Créer un événement")

        if Permission.assign_event(self.user.role):
            choices.append("👤 Assigner un évènement")

        if Permission.update_event(self.user.role):
            choices.append("📝 Ajouter une note à un événement")
            choices.append("✏️  Modifier un événement")

        if Permission.delete_event(self.user.role):
            choices.append("❌ Supprimer un événement")

        choices.extend([BACK_TO_MAIN_MENU] + QUIT_APP_CHOICES)

        while True:
            Utils.display_menu_title("Menu Événement")
            action = Utils.get_questionnary(choices)

            match action:
                case "🗂️  Afficher la liste des événements":
                    self.event_manager.display_all_events_menu()
                    continue
                case "🎫 Afficher un événement":
                    self.event_manager.display_event()
                    continue
                case "🆕 Créer un événement":
                    self.event_manager.create_event()
                    continue
                case "👤 Assigner un évènement":
                    self.event_manager.assign_event()
                    continue
                case "📝 Ajouter une note à un événement":
                    self.event_manager.add_note()
                    continue
                case "✏️  Modifier un événement":
                    self.event_manager.update_event()
                    continue
                case "❌ Supprimer un événement":
                    self.event_manager.delete_event()
                    continue
                case "🔙 Retour au menu principal":
                    break
                case "🔒 Déconnexion":
                    AuthManager.logout()
                    break
                case "❌ Quitter l'application":
                    Utils.quit_app()
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

        choices = [
            "Créer ou mettre à jour les tables",
            "Créer un rôle",
            "Supprimer les tables",
            "Quitter l'application"
        ]

        while True:
            action = Utils.get_questionnary(choices)

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
