from .text import TextManager


class WarningMessage():
    color = "yellow"

    @classmethod
    def action_cancelled(cls):
        print(
            TextManager.color(
                "Action annulée.",
                cls.color
            )
        )

    @classmethod
    def cancel_command_info(cls):
        print(
            TextManager.color(
                "(Appuyez sur Ctrl+C pour annuler)",
                cls.color
            )
        )

    @classmethod
    def empty_table(cls, model_name):
        print(
            TextManager.color(
                f"La table '{model_name}' est vide.",
                cls.color
            )
        )

    @classmethod
    def no_table_update(cls):
        print(
            TextManager.color(
                "Toutes les tables sont déjà à jour.",
                cls.color
            )
        )
