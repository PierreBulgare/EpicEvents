from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from datetime import datetime

from models import Role, Collaborateur, Client, Contrat, Evenement
from security import hash_password

# Chargement de l'environnement
load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

# Connexion à la base de données
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Création des rôles
roles = ["commercial", "gestion", "support"]
for nom_role in roles:
    role = session.query(Role).filter_by(nom=nom_role).first()
    if not role:
        session.add(Role(nom=nom_role))

session.commit()

# Récupération des rôles
role_commercial = session.query(Role).filter_by(nom="commercial").first()
role_gestion = session.query(Role).filter_by(nom="gestion").first()
role_support = session.query(Role).filter_by(nom="support").first()

# Création de collaborateurs
collab_commercial = Collaborateur(
    nom="Alice Commercial",
    email="alice@epicevents.com",
    role=role_commercial,
    password_hash=hash_password("password1")
)

collab_gestion = Collaborateur(
    nom="Bob Gestion",
    email="bob@epicevents.com",
    role=role_gestion,
    password_hash=hash_password("password2")
)

collab_support = Collaborateur(
    nom="Charlie Support",
    email="charlie@epicevents.com",
    role=role_support,
    password_hash=hash_password("password3")
)

session.add_all([collab_commercial, collab_gestion, collab_support])
session.commit()

# Création d'un client associé au commercial
client = Client(
    nom_complet="John Doe",
    email="john.doe@example.com",
    telephone="+33123456789",
    nom_entreprise="Doe Industries",
    date_creation=datetime.now(),
    derniere_maj=datetime.now(),
    contact_commercial=collab_commercial
)
session.add(client)
session.commit()

# Création d'un contrat associé au client, créé par gestionnaire
contrat = Contrat(
    client=client,
    montant_total=10000.0,
    montant_restant=5000.0,
    date_creation=datetime.now(),
    statut_signe=True,
    contact_gestion=collab_gestion
)
session.add(contrat)
session.commit()

# Création d'un événement

evenement = Evenement(
    contrat=contrat,
    date_debut=datetime(2024, 7, 15, 10, 0),
    date_fin=datetime(2024, 7, 15, 18, 0),
    lieu="Centre de congrès, Paris",
    nombre_participants=250,
    notes="Prévoir une restauration complète et équipements multimédias.",
    contact_commercial=collab_commercial,
    contact_support=collab_support
)
session.add(evenement)
session.commit()

# Affichage pour vérification
print("Données insérées :")
for evt in session.query(Evenement).all():
    print(f"Événement : {evt.id}, Lieu : {evt.lieu}")
    print(f"  Commercial : {evt.contact_commercial.nom}")
    print(f"  Support : {evt.contact_support.nom}")
    print(f"  Client : {evt.contrat.client.nom_complet}")
    print(f"  Créé par (gestion) : {evt.contrat.contact_gestion.nom}")

session.close()
