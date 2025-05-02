import os
import sys
from settings import APP_TITLE, APP_VERSION, AUTHOR
from managers.message import MessageManager
from auth import logout


def display_app_title(user, admin=False):
    width = 50
    print("=" * width)
    print(f"{APP_TITLE:^{width}}")
    print(f"{'Version: ' + APP_VERSION:^{width}}")
    print(f"{'Author: ' + AUTHOR:^{width}}")
    print("=" * width)

    if not admin:
        if hasattr(user, 'name'):
            MessageManager.welcome_message(user)
    else:
        print("Bienvenue dans l'espace Administrateur !")


def new_screen(user, admin=False):
    os.system('cls' if os.name == 'nt' else 'clear')
    display_app_title(user, admin)


def quit_app(user_logout=False):
    if user_logout:
        logout()
    MessageManager.end_program()
    sys.exit(0)

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