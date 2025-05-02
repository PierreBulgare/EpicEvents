import sys
import os

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    )

from models_managers.database import DatabaseManager
from utils.auth import AuthManager
from utils.utils import Utils
from utils.menu import MenuManager
from messages_managers.text import TextManager


def run():
    TextManager.init_colorama()
    Utils.init_sentry()
    Utils.new_screen(None, admin=True)
    AuthManager.login_admin()
    MenuManager(DatabaseManager()).admin_menu()


if __name__ == "__main__":
    run()
