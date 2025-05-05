from .text import TextManager
from app.settings import ROLES


class ErrorMessage():
    color = "red"

    @classmethod
    def invalid_email(cls):
        print(
            TextManager.color(
                "L'email fourni est invalide.",
                cls.color
            )
        )

    @classmethod
    def email_empty(cls):
        print(
            TextManager.color(
                "L'email ne peut pas être vide.",
                cls.color
            )
        )

    @classmethod
    def client_email_already_exists(cls, email):
        print(
            TextManager.color(
                f"L'email {email} est déjà utilisé pour un autre client.",
                cls.color
            )
        )

    @classmethod
    def username_empty(cls):
        print(
            TextManager.color(
                "Vous n'avez pas renseigné votre nom.",
                cls.color
            )
        )

    @classmethod
    def user_firstname_empty(cls):
        print(
            TextManager.color(
                "Vous n'avez pas renseigné votre prénom.",
                cls.color
            )
        )

    @classmethod
    def password_empty(cls):
        print(
            TextManager.color(
                "Le mot de passe ne peut pas être vide.",
                cls.color
            )
        )

    @classmethod
    def password_too_short(cls):
        print(
            TextManager.color(
                "Le mot de passe doit contenir au moins 8 caractères.",
                cls.color
            )
        )

    @classmethod
    def invalid_token(cls):
        print(
            TextManager.color(
                "Le token est invalide ou a expiré.",
                cls.color
            )
        )

    @classmethod
    def token_not_found(cls):
        print(
            TextManager.color(
                "Token introuvable. Vous devez vous connecter.",
                cls.color
            )
        )

    @classmethod
    def action_not_recognized(cls):
        print(
            TextManager.color(
                "Action non reconnue. Veuillez réessayer.",
                cls.color
            )
        )

    @classmethod
    def database_error(cls):
        print(
            TextManager.color(
                "Erreur de base de données. Veuillez réessayer.",
                cls.color
            )
        )

    @classmethod
    def account_not_found(cls, email):
        print(
            TextManager.color(
                f"Aucun compte trouvé avec l'email : {email}.",
                cls.color
            )
        )


    @classmethod
    def data_not_found(cls, data_type, data_value):
        print(
            TextManager.color(
                f"{data_type} '{data_value}' introuvable. "
                "Veuillez vérifier les informations fournies.",
                cls.color
            )
        )

    @classmethod
    def table_not_found(cls, table_name):
        print(
            TextManager.color(
                f"La table '{table_name}' n'existe pas.",
                cls.color
            )
        )

    @classmethod
    def tables_already_exist(cls):
        print(
            TextManager.color(
                "Les tables existent déjà.",
                cls.color
            )
        )

    @classmethod
    def session_close_error(cls, error):
        print(
            TextManager.color(
                f"Erreur lors de la fermeture de la session : {error}",
                cls.color
            )
        )

    @classmethod
    def account_already_exists(cls):
        print(
            TextManager.color(
                "Un compte avec cet email existe déjà.",
                cls.color
            )
        )

    @classmethod
    def invalid_credentials(cls):
        print(
            TextManager.color(
                "Email ou mot de passe incorrect.",
                cls.color
            )
        )

    @classmethod
    def role_not_found(cls, role_name):
        print(
            TextManager.color(
                f"Rôle '{role_name}' introuvable.",
                cls.color
            )
        )

    @classmethod
    def role_already_exists(cls, role_name):
        print(
            TextManager.color(
                f"Le rôle '{role_name}' existe déjà.",
                cls.color
            )
        )

    @classmethod
    def role_empty(cls):
        print(
            TextManager.color(
                "Le nom du rôle ne peut pas être vide.",
                cls.color
            )
        )

    @classmethod
    def invalid_role(cls):
        print(
            TextManager.color(
                f"Rôle invalide. Veuillez choisir parmi : {', '.join(ROLES)}",
                cls.color
            )
        )

    @classmethod
    def contract_already_signed(cls, contract_id):
        print(
            TextManager.color(
                f"Le contrat {contract_id} a déjà été signé.",
                cls.color
            )
        )

    @classmethod
    def contract_already_linked(cls, event):
        print(
            TextManager.color(
                f"Ce contrat est déjà lié à l'événement {event.nom} ({event.id}).",
                cls.color
            )
        )

    @classmethod
    def invalid_id(cls):
        print(
            TextManager.color(
                "L'ID fourni est invalide.",
                cls.color
            )
        )

    @classmethod
    def contract_client_mismatch(cls, contract_id, client):
        print(
            TextManager.color(
                f"Le contrat {contract_id} n'appartient pas au client "
                f"{client.nom_complet} ({client.id})",
                cls.color
            )
        )

    @classmethod
    def client_name_empty(cls):
        print(
            TextManager.color(
                "Le nom du client ne peut pas être vide.",
                cls.color
            )
        )

    @classmethod
    def collab_role_mismatch(cls, name, role_name):
        print(
            TextManager.color(
                f"Le collaborateur {name} ne fait pas partie du département '{role_name}'.",
                cls.color
            )
        )

    @classmethod
    def event_name_empty(cls):
        print(
            TextManager.color(
                "Le nom de l'événement ne peut pas être vide.",
                cls.color
            )
        )

    @classmethod
    def event_location_empty(cls):
        print(
            TextManager.color(
                "Le lieu de l'événement ne peut pas être vide.",
                cls.color
            )
        )

    @classmethod
    def event_start_date_empty(cls):
        print(
            TextManager.color(
                "La date de début de l'événement ne peut pas être vide.",
                cls.color
            )
        )

    @classmethod
    def event_end_date_empty(cls):
        print(
            TextManager.color(
                "La date de fin de l'événement ne peut pas être vide.",
                cls.color
            )
        )

    @classmethod
    def event_attendees_empty(cls):
        print(
            TextManager.color(
                "Le nombre de participants ne peut pas être vide.",
                cls.color
            )
        )

    @classmethod
    def event_note_empty(cls):
        print(
            TextManager.color(
                "La note ne peut pas être vide.",
                cls.color
            )
        )

    @classmethod
    def invalid_date_format(cls):
        print(
            TextManager.color(
                "Le format de la date est invalide. "
                "Veuillez utiliser le format 'JJ-MM-AAAA'.",
                cls.color
            )
        )

    @classmethod
    def end_date_before_start_date(cls):
        print(
            TextManager.color(
                "La date de fin ne peut pas être antérieure à la date de début.",
                cls.color
            )
        )

    @classmethod
    def end_date_before_today(cls):
        print(
            TextManager.color(
                "La date de fin ne peut pas être antérieure à la date actuelle.",
                cls.color
            )
        )

    @classmethod
    def start_date_before_today(cls):
        print(
            TextManager.color(
                "La date de début ne peut pas être antérieure à la date actuelle.",
                cls.color
            )
        )

    @classmethod
    def start_date_after_end_date(cls):
        print(
            TextManager.color(
                "La date de début ne peut pas être postérieure à la date de fin.",
                cls.color
            )
        )

    @classmethod
    def invalid_amount(cls):
        print(
            TextManager.color(
                f"Le montant est invalide.",
                cls.color
            )
        )

    @classmethod
    def amount_negative(cls):
        print(
            TextManager.color(
                f"Le montant ne peut pas être négatif.",
                cls.color
            )
        )

    @classmethod
    def invalid_attendees_number(cls):
        print(
            TextManager.color(
                f"Le nombre de participants est invalide.",
                cls.color
            )
        )

    @classmethod
    def remaining_gt_total(cls):
        print(
            TextManager.color(
                f"Le montant restant dû ne peut pas être supérieur "
                f"au montant total.",
                cls.color
            )
        )

    @classmethod
    def id_empty(cls):
        print(
            TextManager.color(
                "L'ID ne peut pas être vide.",
                cls.color
            )
        )

    @classmethod
    def admin_password_empty(cls):
        print(
            TextManager.color(
                "Le mot de passe ne peut pas être vide.",
                cls.color
            )
        )

    @classmethod
    def admin_password_incorrect(cls):
        print(
            TextManager.color(
                "Mot de passe incorrect. Veuillez réessayer.",
                cls.color
            )
        )
