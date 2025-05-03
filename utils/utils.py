import os
import sys
import time
from app.settings import APP_TITLE, APP_VERSION, AUTHOR
from messages_managers.info import InfoMessage
from .auth import AuthManager


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
    def quit_app(user_logout=False):
        if user_logout:
            AuthManager.logout()
        InfoMessage.end_program()
        time.sleep(1)
        sys.exit(0)

    @staticmethod
    def init_sentry():
        import sentry_sdk
        from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

        sentry_sdk.init(
            dsn=(
                "https://7c297ddfd49dbcc4fb3f91aa64bc8680@o4509118924128256."
                "ingest.de.sentry.io/4509118928453712"
            ),
            integrations=[SqlalchemyIntegration()],
            traces_sample_rate=1.0,
        )
