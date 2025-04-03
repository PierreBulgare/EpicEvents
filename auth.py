from models import Collaborateur
from security import verify_password
from jwt_utils import creer_token
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import sys
from dotenv import load_dotenv
from security import hash_password
from models import Role

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()
TOKEN_PATH = os.path.join(os.path.dirname(__file__), ".token")

def create_account():
    # Suppression du token précédent
    with open(TOKEN_PATH, "w") as f:
        f.truncate(0)

    # Demande de l'email et du mot de passe
    nom = input("Nom : ")
    role_nom = input("Rôle (commercial, gestion, support) : ")
    email = input("Email : ")
    password = input("Mot de passe : ")

    # Récupération du rôle
    role = session.query(Role).filter_by(nom=role_nom).first()
    if not role:
        print(f"Le rôle '{role_nom}' n'existe pas.")
        return

    # Vérification si l'email existe déjà
    collaborateur = session.query(Collaborateur).filter_by(email=email).first()
    if collaborateur:
        print("Cet email est déjà utilisé.")
        return

    # Création du collaborateur
    new_collaborateur = Collaborateur(email=email, password_hash=hash_password(password), nom=nom, role=role)
    session.add(new_collaborateur)
    session.commit()
    print("Compte créé avec succès !")
    collaborateur = session.query(Collaborateur).filter_by(email=email).first()
    if collaborateur and verify_password(password, collaborateur.password_hash.encode('utf-8')):
        token = creer_token(collaborateur.id, collaborateur.role.nom)
        print("Authentification réussie !")

        # Enregistrement du token dans .token
        with open(TOKEN_PATH, "w") as f:
            f.write(token)
    else:
        print("Email ou mot de passe incorrect.")

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
