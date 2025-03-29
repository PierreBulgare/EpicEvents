from models import Collaborateur
from security import verify_password
from jwt_utils import creer_token
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import sys
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()
TOKEN_PATH = os.path.join(os.path.dirname(__file__), ".token")

def login():
    # Suppression du token précédent
    with open(TOKEN_PATH, "w") as f:
        f.truncate(0)

    # Boucle de connexion
    while os.path.getsize(TOKEN_PATH) == 0:
        print("Veuillez vous connecter :")
        # Demande de l'email et du mot de passe
        email = input("Email : ")
        password = input("Mot de passe : ")


        collaborateur = session.query(Collaborateur).filter_by(email=email).first()

        # Vérification de l'email et du mot de passe
        if collaborateur and verify_password(password, collaborateur.password_hash.encode('utf-8')):
            token = creer_token(collaborateur.id, collaborateur.role.nom)
            print("Authentification réussie !")

            # Enregistrement du token dans .token
            with open(TOKEN_PATH, "w") as f:
                f.write(token)
        else:
            print("Email ou mot de passe incorrect.")


def logout():
    # Suppression du token
    if os.path.exists(TOKEN_PATH) and os.path.getsize(TOKEN_PATH) > 0:
        with open(TOKEN_PATH, "w") as f:
            f.truncate(0)
        print("Déconnexion réussie !")
    else:
        print("Aucun token trouvé. Vous n'êtes pas connecté.")


if __name__ == "__main__":
    if sys.argv[1] == "login":
        login()
    elif sys.argv[1] == "logout":
        logout()
    else:
        print("Commande non reconnue. Utilisez 'login' ou 'logout'.")
