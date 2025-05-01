import sentry_sdk
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from managers import DatabaseManager, MenuManager
from auth import login_admin
import utils

sentry_sdk.init(
    dsn="https://7c297ddfd49dbcc4fb3f91aa64bc8680@o4509118924128256.ingest.de.sentry.io/4509118928453712",
    integrations=[SqlalchemyIntegration()],
    traces_sample_rate=1.0,
)

menu_manager = MenuManager(DatabaseManager())

def run():
    utils.new_screen(None, admin=True)
    login_admin()
    menu_manager.admin_menu()
    
if __name__ == "__main__":
    run()