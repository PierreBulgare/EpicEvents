from .text import TextManager
from settings import APP_TITLE

class MessageManager:
    error_color = "red"
    success_color = "green"
    info_color = "blue"
    warning_color = "yellow"

    """ Messages communs"""
    @classmethod
    # Messages d'information
    def end_program(cls):
        print(TextManager.color(f"Merci d'avoir utilisé l'application {APP_TITLE} !", cls.info_color))

    @classmethod
    def welcome_message(cls, user):
        print(f"Bonjour {TextManager.color(user.name, cls.info_color)} !")
        print(f"Vous êtes connecté en tant que membre du département {TextManager.color(user.role, cls.info_color)}.")

    # Messages de succès
    @classmethod
    def create_success(cls):
        print(TextManager.color(f"Création effectuée avec succès !", cls.success_color))

    @classmethod
    def update_success(cls):
        print(TextManager.color(f"Mise à jour effectuée avec succès !", cls.success_color))

    @classmethod
    def delete_success(cls):
        print(TextManager.color(f"Suppression effectuée avec succès !", cls.success_color))

    @classmethod
    def logout_success(cls):
        print(TextManager.color("Vous êtes déconnecté avec succès !", cls.success_color))

    # Messages d'erreur
    @classmethod
    def invalid_token(cls):
        print(TextManager.color("Le token est invalide ou a expiré.", cls.error_color))

    @classmethod
    def token_not_found(cls):
        print(TextManager.color("Token introuvable. Vous devez vous connecter.", cls.error_color))

    @classmethod
    def action_not_recognized(cls):
        print(TextManager.color("Action non reconnue. Veuillez réessayer.", cls.error_color))

    @classmethod
    def data_not_found(cls, data_type, data_value):
        print(TextManager.color(f"{data_type} '{data_value}' introuvable. Veuillez vérifier les informations fournies.", cls.error_color))

    # Messages d'avertissement
    @classmethod
    def action_cancelled(cls):
        print(TextManager.color("Action annulée.", cls.warning_color))

    @classmethod
    def cancel_command_info(cls):
        print(TextManager.color("(Appuyez sur Ctrl+C pour annuler)", cls.warning_color))

    @classmethod
    def empty_table(cls, model_name):
        print(TextManager.color(f"La table '{model_name}' est vide.", cls.warning_color))

    """ Messages Base de données"""
    # Messages de succès
    @classmethod
    def tables_created(cls):
        print(TextManager.color("Les tables ont été créées avec succès !", cls.success_color))

    @classmethod
    def tables_dropped(cls):
        print(TextManager.color("Les tables ont été supprimées avec succès !", cls.success_color))

    @classmethod
    def column_added(cls, table_name, column_name):
        print(TextManager.color(f"La colonne '{column_name}' a été ajoutée à la table '{table_name}' avec succès !", cls.success_color))

    # Messages d'erreur
    @classmethod
    def table_not_found(cls, table_name):
        print(TextManager.color(f"La table '{table_name}' n'existe pas.", cls.error_color))

    @classmethod
    def tables_already_exist(cls):
        print(TextManager.color("Les tables existent déjà.", cls.error_color))

    @classmethod
    def session_close_error(cls, error):
        print(TextManager.color(f"Erreur lors de la fermeture de la session : {error}", cls.error_color))

    """ Messages Collaborateur"""
    # Message de succès
    @classmethod
    def account_created(cls):
        print(TextManager.color("Votre compte a été créé avec succès !", cls.success_color))

    # Messages d'erreur
    @classmethod
    def account_already_exists(cls):
        print(TextManager.color("Un compte avec cet email existe déjà.", cls.error_color))
    
    @classmethod
    def invalid_role(cls):
        print(TextManager.color("Rôle invalide. Veuillez choisir parmi : Commercial, Gestion, Support.", cls.error_color))

    @classmethod
    def invalid_credentials(cls):
        print(TextManager.color("Email ou mot de passe incorrect.", cls.error_color))

    """ Messages Rôle """
    # Messages de succès
    @classmethod
    def role_created(cls, role_name):
        print(TextManager.color(f"Le rôle '{role_name}' a été créé avec succès !", cls.success_color))

    # Messages d'erreur
    @classmethod
    def role_not_found(cls, role_name):
        print(TextManager.color(f"Rôle '{role_name}' introuvable.", cls.error_color))

    @classmethod
    def role_already_exists(cls, role_name):
        print(TextManager.color(f"Le rôle '{role_name}' existe déjà.", cls.error_color))

    @classmethod
    def role_empty(cls):
        print(TextManager.color("Le nom du rôle ne peut pas être vide.", cls.error_color))

    """ Messages Contrat """
    # Messages de succès
    @classmethod
    def sign_success(cls, contract_id):
        print(TextManager.color(f"Le contrat {contract_id} a été signé avec succès !", cls.success_color))

    # Messages d'erreur
    @classmethod
    def contract_already_signed(cls, contract_id):
        print(TextManager.color(f"Le contrat {contract_id} a déjà été signé.", cls.error_color))

    @classmethod
    def contract_client_mismatch(cls, contract_id, client):
        print(TextManager.color(f"Le contrat {contract_id} n'appartient pas au client {client.nom_complet} ({client.id})", cls.error_color))

    """ Messages Espace Administrateur """
    # Messages d'erreur
    @classmethod
    def admin_password_empty(cls):
        print(TextManager.color("Le mot de passe ne peut pas être vide.", cls.error_color))

    @classmethod
    def admin_password_incorrect(cls):
        print(TextManager.color("Mot de passe incorrect. Veuillez réessayer.", cls.error_color))
    
