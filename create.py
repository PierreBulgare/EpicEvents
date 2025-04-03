from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
import sys
from datetime import datetime

from models import Role, Collaborateur, Client, Contrat, Evenement
from security import hash_password
from jwt_utils import verifier_token, verifier_role





# Chargement de l'environnement
load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

# Connexion à la base de données
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

TOKEN_PATH = os.path.join(os.path.dirname(__file__), ".token")

def new_role(nom_role):
    role = session.query(Role).filter_by(nom=nom_role).first()
    if not role:
        role = Role(nom=nom_role)
        session.add(role)
        session.commit()
        print(f"Rôle '{nom_role}' créé avec succès.")
    else:
        print(f"Le rôle '{nom_role}' existe déjà.")
    return role

def new_collaborateur():
    nom = input("Nom : ")
    email = input("Email : ")
    password = input("Mot de passe : ")
    role_nom = input("Rôle (commercial, gestion, support) : ")

    # Récupération du rôle
    role = session.query(Role).filter_by(nom=role_nom).first()
    if not role:
        print(f"Le rôle '{role_nom}' n'existe pas.")
        return

    # Création du collaborateur
    collaborateur = Collaborateur(
        nom=nom,
        email=email,
        role=role,
        password_hash=hash_password(password)
    )
    session.add(collaborateur)
    session.commit()
    print(f"Collaborateur '{nom} | {email}' créé avec succès.")

def new_client():
    if os.path.getsize(TOKEN_PATH) == 0:
        print("Vous devez être connecté pour créer un client.")
        return
    with open(TOKEN_PATH, "r") as f:
        token = f.read().strip()
    payload = verifier_token(token)
    if payload is None:
        print("Token invalide ou expiré.")
        return
    if not verifier_role(token, "commercial"):
        print("Vous n'avez pas les droits nécessaires pour créer un client.")
        return

    nom_complet = input("Nom complet : ")
    email = input("Email : ")
    telephone = input("Téléphone : ")
    nom_entreprise = input("Nom de l'entreprise : ")

    # Création du client
    client = Client(
        nom_complet=nom_complet,
        email=email,
        telephone=telephone,
        nom_entreprise=nom_entreprise,
        date_creation=datetime.now(),
        derniere_maj=datetime.now(),
        contact_commercial=session.query(Collaborateur).filter_by(id=payload["user_id"]).first()
    )
    session.add(client)
    session.commit()
    print(f"Client '{nom_complet}' créé avec succès.")


def new_contrat(client_id):
    if os.path.getsize(TOKEN_PATH) == 0:
        print("Vous devez être connecté pour créer un client.")
        return
    with open(TOKEN_PATH, "r") as f:
        token = f.read().strip()
    payload = verifier_token(token)
    if payload is None:
        print("Token invalide ou expiré.")
        return
    if not verifier_role(token, "gestion"):
        print("Vous n'avez pas les droits nécessaires pour créer un contrat.")
        return
    
    montant_total = float(input("Montant total : "))

    # Récupération du client
    client = session.query(Client).filter_by(id=client_id).first()
    if not client:
        print(f"Le client avec ID '{client_id}' n'existe pas.")
        return

    # Création du contrat
    contrat = Contrat(
        client=client,
        montant_total=montant_total,
        montant_restant=montant_total,
        date_creation=datetime.now(),
        contact_gestion=session.query(Collaborateur).filter_by(id=payload["user_id"]).first()
    )
    session.add(contrat)
    session.commit()
    print(f"Contrat créé avec succès pour le client '{client.nom_complet}'.")


if __name__ == "__main__":
    if sys.argv[1] == "role":
        if len(sys.argv) > 2:
            for arg in sys.argv[2:]:
                new_role(arg)
    elif sys.argv[1] == "collab":
        new_collaborateur()
    elif sys.argv[1] == "client":
        new_client()
    elif sys.argv[1] == "contrat":
        if len(sys.argv) > 2:
            new_contrat(int(sys.argv[2]))
        else:
            print("Veuillez fournir l'ID du client.")