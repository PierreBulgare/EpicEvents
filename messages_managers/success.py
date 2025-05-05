from .text import TextManager


class SuccessMessage():
    color = "green"

    @classmethod
    def create_success(cls, *args):
        print(
            TextManager.color(
                "Création effectuée avec succès !",
                cls.color
            )
        )

    @classmethod
    def collab_created(cls, name):
        print(
            TextManager.color(
                f"Collaborateur {name} effectuée avec succès !",
                cls.color
            )
        )

    @classmethod
    def update_success(cls, *args):
        print(
            TextManager.color(
                "Mise à jour effectuée avec succès !",
                cls.color
            )
        )

    @classmethod
    def assign_success(cls, event, support):
        print(
            TextManager.color(
                f"Assignation de l'événement {event} au support {support} ",
                cls.color
            )
        )

    @classmethod
    def event_note_success(cls):
        print(
            TextManager.color(
                f"Note ajoutée avec succès !",
                cls.color
            )
        )

    @classmethod
    def delete_success(cls, *args):
        print(
            TextManager.color(
                "Suppression effectuée avec succès !",
                cls.color
            )
        )

    @classmethod
    def logout_success(cls):
        print(
            TextManager.color(
                "Vous êtes déconnecté avec succès !",
                cls.color
            )
        )

    @classmethod
    def token_saved(cls):
        print(
            TextManager.color(
                "Le token a été enregistré avec succès !",
                cls.color
            )
        )

    """ Messages Base de données """
    @classmethod
    def table_created(cls, table_name):
        print(
            TextManager.color(
                f"La table '{table_name}' a été créée avec succès !",
                cls.color
            )
        )

    @classmethod
    def tables_dropped(cls):
        print(
            TextManager.color(
                "Les tables ont été supprimées avec succès !",
                cls.color
            )
        )

    @classmethod
    def column_added(cls, table_name, column_name):
        print(
            TextManager.color(
                f"La colonne '{column_name}' a été ajoutée à la table "
                f"'{table_name}' avec succès !",
                cls.color
            )
        )

    """ Messages Collaborateur """
    @classmethod
    def account_created(cls):
        print(
            TextManager.color(
                "Votre compte a été créé avec succès !",
                cls.color
            )
        )

    """ Messages Rôle """
    @classmethod
    def role_created(cls, role_name):
        print(
            TextManager.color(
                f"Le rôle '{role_name}' a été créé avec succès !",
                cls.color
            )
        )

    """ Messages Contrat """
    @classmethod
    def sign_success(cls, contract_id):
        print(
            TextManager.color(
                f"Le contrat {contract_id} a été signé avec succès !",
                cls.color
            )
        )
