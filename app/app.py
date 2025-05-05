import sys
import os

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    )

from utils.menu import MenuManager
from utils.utils import Utils
from models_managers.database import DatabaseManager
from models_managers.user import UserManager
from messages_managers.text  import TextManager


def run():
    TextManager.init_colorama()
    Utils.init_sentry()
    while True:
        menu_manager = MenuManager(DatabaseManager(), UserManager())
        menu_manager.main_page()
        menu_manager.main_menu()


if __name__ == "__main__":
    run()
