import os
import sys
from datetime import datetime
import questionary
import random
import string
from app.settings import APP_TITLE, APP_VERSION, AUTHOR, SENTRY_DSN
from messages_managers.info import InfoMessage
from messages_managers.text import TextManager
from messages_managers.warning import WarningMessage
from messages_managers.error import ErrorMessage


class Utils:
    @staticmethod
    def display_app_title(user, admin=False):
        width = os.get_terminal_size().columns
        print("=" * width)
        print(f"{APP_TITLE:^{width}}")
        print(f"{'Version: ' + APP_VERSION:^{width}}")
        print(f"{'Author: ' + AUTHOR:^{width}}")
        print("=" * width)

        if not admin:
            if hasattr(user, 'name'):
                InfoMessage.welcome_message(user)
        else:
            print("Bienvenue dans l'espace Administrateur !")

    @classmethod
    def new_screen(cls, user, admin=False):
        os.system('cls' if os.name == 'nt' else 'clear')
        cls.display_app_title(user, admin)

    @staticmethod
    def quit_app():
        InfoMessage.end_program()
        # time.sleep(1)
        sys.exit(0)

    @staticmethod
    def init_sentry():
        import sentry_sdk
        from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

        sentry_sdk.init(
            dsn=SENTRY_DSN,
            integrations=[SqlalchemyIntegration()],
            traces_sample_rate=1.0,
            send_default_pii=True
        )

    @staticmethod
    def get_questionnary(choices=None, edit=False, delete=False):
        if edit:
            question = "Que voulez-vous modifier ?"
        elif delete:
            choices = ["Confirmer", "Annuler"]
            question = "Confirmez-vous la suppression ?"
        else:
            question = "Que voulez-vous faire ?"
        return questionary.select(
            question,
            choices=choices,
            use_shortcuts=True,
            instruction=" ",
        ).ask()

    @staticmethod
    def get_input(field, default=""):
        return questionary.text(
            field,
            default=default,
        ).ask()

    @classmethod
    def confirm_deletion(cls):
        while True:
            confirmation = cls.get_questionnary(delete=True)
            match confirmation:
                case "Confirmer":
                    return True
                case "Annuler":
                    WarningMessage.action_cancelled()
                    return False
                case _:
                    ErrorMessage.action_not_recognized()

    @staticmethod
    def email_is_valid(email: str) -> bool:
        if "@" not in email:
            return False
        if "." not in email.split("@")[-1]:
            return False
        if email.endswith("."):
            return False
        return True

    @staticmethod
    def date_is_valid(date):
        try:
            datetime.strptime(date, "%d-%m-%Y")
            return True
        except ValueError:
            return False

    @staticmethod
    def display_menu_title(title):
        print(TextManager.style(
            TextManager.color(title, "magenta"),
            "bold"))

    @staticmethod
    def generate_password(length=8):
        """
        Génère un mot de passe aléatoire.
        """
        while True:
            characters = (
                string.ascii_letters + string.digits + string.punctuation
            )
            password = ''.join(random.sample(characters, length))

            if (any(c.isalpha() for c in password) and
                any(c.isdigit() for c in password) and
                    any(c in string.punctuation for c in password)):
                return password
