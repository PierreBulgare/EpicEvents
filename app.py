import utils
from managers import DatabaseManager, UserManager, MenuManager


def run():
    utils.init_sentry()
    menu_manager = MenuManager(DatabaseManager(), UserManager())
    menu_manager.main_page()
    menu_manager.main_menu()


if __name__ == "__main__":
    run()
