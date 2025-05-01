import sentry_sdk
from settings import APP_TITLE, APP_VERSION, TOKEN_PATH
from managers import (
    DatabaseManager, UserManager, ClientManager, ContractManager,
    MenuManager
)
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

sentry_sdk.init(
    dsn="https://7c297ddfd49dbcc4fb3f91aa64bc8680@o4509118924128256.ingest.de.sentry.io/4509118928453712",
    integrations=[SqlalchemyIntegration()],
    traces_sample_rate=1.0,
)

db_manager = DatabaseManager()
user = UserManager()
menu_manager = MenuManager(db_manager, user)

def run():
    menu_manager.main_page()
    menu_manager.main_menu()

if __name__ == "__main__":
    run()
