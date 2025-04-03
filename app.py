import questionary
import subprocess
import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from jwt_utils import verifier_token
from auth import login, create_account, logout

# Chargement de l'environnement
load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

# Connexion à la base de données
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

TOKEN_PATH = os.path.join(os.path.dirname(__file__), ".token")

app_title = "EPIC Events"
app_version = "1.0.0"
MAIN_CHOICES = [
    "Gérer les clients",
    "Gérer les contrats",
    "Gérer les événements",
    "Quitter l'application (Sans Déconnexion)",
    "Quitter l'application (Avec Déconnexion)"
]

def main_page():
    print("Bienvenue dans l'application EPIC Events !")
    if os.path.getsize(TOKEN_PATH) == 0:
            action = questionary.select(
            "Choisissez une action",
            choices=["Se connecter", "Créer un compte"],
            use_shortcuts=True,
        ).ask()
            match action:
                case "Se connecter":
                    login()
                case "Créer un compte":
                    create_account()
    else:
        with open(TOKEN_PATH, "r") as f:
            token = f.read().strip()
        payload = verifier_token(token)
        if payload is None:
            print("Token invalide ou expiré. Veuillez-vous reconnecter.")
            login()

def main_menu():
    action = questionary.select(
        "Menu Principal",
        choices=MAIN_CHOICES,
        use_shortcuts=True,
    ).ask()

    match action:
        case "Gérer les clients":
            manage_clients()
        case "Quitter l'application (Sans Déconnexion)":
            print("Merci d'avoir utilisé l'application EPIC Events !")
            sys.exit(0)
        case "Quitter l'application (Avec Déconnexion)":
            logout()
            print("Merci d'avoir utilisé l'application EPIC Events !")
            sys.exit(0)
    
def manage_clients():
    CHOICES = [
        "Ajouter un client",
        "Modifier un client",
        "Supprimer un client",
        "Retourner au menu principal"
    ]

    action = questionary.select(
        "Menu Principal",
        choices=CHOICES,
        use_shortcuts=True,
    ).ask()

    match action:
        case "Ajouter un client":
            subprocess.run([sys.executable, "create.py", "client"])

def run():
    print(f"{'=' * 55}\n{app_title}\nVersion: {app_version}\n{'=' * 55}")
    main_page()
    main_menu()


if __name__ == "__main__":
    run()