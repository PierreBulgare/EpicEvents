import os
from dotenv import load_dotenv

load_dotenv()

# Variables constantes
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "default_secret")
DATABASE_URL = os.getenv('DATABASE_URL')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')
TOKEN_PATH = os.path.join(os.path.dirname(__file__), ".token")
SENTRY_DSN = os.getenv("SENTRY_DSN")
APP_TITLE = "EPIC Events"
APP_VERSION = "1.0.0"
AUTHOR = "Pierre BULGARE"
QUIT_APP_CHOICES = [
    "🔒 Déconnexion",
    "❌ Quitter l'application"
    ]
ROLES = ["Commercial", "Gestion", "Support"]
BACK_TO_MAIN_MENU = "🔙 Retour au menu principal"
