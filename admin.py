import utils
from managers import DatabaseManager, MenuManager
from auth import login_admin


def run():
    utils.init_sentry()
    utils.new_screen(None, admin=True)
    login_admin()
    MenuManager(DatabaseManager()).admin_menu()


if __name__ == "__main__":
    run()
