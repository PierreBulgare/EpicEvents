from .text import TextManager
from settings import ROLES


class ErrorMessage():
    @classmethod
    def invalid_token(cls):
        print(
            TextManager.color(
                "Le token est invalide ou a expiré.",
                cls.error_color
            )
        )

    @classmethod
    def token_not_found(cls):
        print(
            TextManager.color(
                "Token introuvable. Vous devez vous connecter.",
                cls.error_color
            )
        )

    @classmethod
    def action_not_recognized(cls):
        print(
            TextManager.color(
                "Action non reconnue. Veuillez réessayer.",
                cls.error_color
            )
        )

    @classmethod
    def data_not_found(cls, data_type, data_value):
        print(
            TextManager.color(
                f"{data_type} '{data_value}' introuvable. "
                "Veuillez vérifier les informations fournies.",
                cls.error_color
            )
        )

    @classmethod
    def table_not_found(cls, table_name):
        print(
            TextManager.color(
                f"La table '{table_name}' n'existe pas.",
                cls.error_color
            )
        )

    @classmethod
    def tables_already_exist(cls):
        print(
            TextManager.color(
                "Les tables existent déjà.",
                cls.error_color
            )
        )

    @classmethod
    def session_close_error(cls, error):
        print(
            TextManager.color(
                f"Erreur lors de la fermeture de la session : {error}",
                cls.error_color
            )
        )

    @classmethod
    def account_already_exists(cls):
        print(
            TextManager.color(
                "Un compte avec cet email existe déjà.",
                cls.error_color
            )
        )

    @classmethod
    def invalid_credentials(cls):
        print(
            TextManager.color(
                "Email ou mot de passe incorrect.",
                cls.error_color
            )
        )

    @classmethod
    def role_not_found(cls, role_name):
        print(
            TextManager.color(
                f"Rôle '{role_name}' introuvable.",
                cls.error_color
            )
        )

    @classmethod
    def role_already_exists(cls, role_name):
        print(
            TextManager.color(
                f"Le rôle '{role_name}' existe déjà.",
                cls.error_color
            )
        )

    @classmethod
    def role_empty(cls):
        print(
            TextManager.color(
                "Le nom du rôle ne peut pas être vide.",
                cls.error_color
            )
        )

    @classmethod
    def invalid_role(cls):
        print(
            TextManager.color(
                f"Rôle invalide. Veuillez choisir parmi : {', '.join(ROLES)}.",
                cls.error_color
            )
        )

    @classmethod
    def contract_already_signed(cls, contract_id):
        print(
            TextManager.color(
                f"Le contrat {contract_id} a déjà été signé.",
                cls.error_color
            )
        )

    @classmethod
    def contract_client_mismatch(cls, contract_id, client):
        print(
            TextManager.color(
                f"Le contrat {contract_id} n'appartient pas au client "
                f"{client.nom_complet} ({client.id})",
                cls.error_color
            )
        )

    @classmethod
    def admin_password_empty(cls):
        print(
            TextManager.color(
                "Le mot de passe ne peut pas être vide.",
                cls.error_color
            )
        )

    @classmethod
    def admin_password_incorrect(cls):
        print(
            TextManager.color(
                "Mot de passe incorrect. Veuillez réessayer.",
                cls.error_color
            )
        )
