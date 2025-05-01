import os
from dotenv import load_dotenv

load_dotenv()

# Variables constantes
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "default_secret")
DATABASE_URL = os.getenv('DATABASE_URL')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')
TOKEN_PATH = os.path.join(os.path.dirname(__file__), ".token")
APP_TITLE = "EPIC Events"
APP_VERSION = "1.0.0"
QUIT_APP_CHOICES = ["❌ Quitter l'application (Sans Déconnexion)", "🔒 Quitter l'application (Avec Déconnexion)"]