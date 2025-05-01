import os
import sys
from settings import APP_TITLE, APP_VERSION
from managers.message import MessageManager
from auth import logout


def display_app_title(user, admin=False):
    print(f"{'=' * 55}\n{APP_TITLE}\nVersion: {APP_VERSION}\n{'=' * 55}")

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
