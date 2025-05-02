from .text import TextManager
from settings import APP_TITLE


class InfoMessage():
    color = "blue"

    @classmethod
    def end_program(cls):
        print(
            TextManager.color(
                f"Merci d'avoir utilisé l'application {APP_TITLE} !",
                cls.color
            )
        )

    @classmethod
    def welcome_message(cls, user):
        print(
            f"Bonjour {TextManager.color(user.name, cls.color)} !"
        )
        print(
            f"Vous êtes connecté en tant que membre du département "
            f"{TextManager.color(user.role, cls.color)}."
        )
