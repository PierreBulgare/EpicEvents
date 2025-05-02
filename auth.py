from models import Collaborateur
from security import verify_password
from jwt_utils import create_token, delete_token, save_token
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from security import hash_password
from models import Role
from managers.error_message import ErrorMessage
from managers.success_message import SuccessMessage
import pwinput
from settings import ADMIN_PASSWORD

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()
TOKEN_PATH = os.path.join(os.path.dirname(__file__), ".token")

def create_account():
    delete_token()

    nom = input("Nom : ")
    role_nom = input("Rôle (Commercial, Gestion, Support) : ").capitalize()
    email = input("Email : ")
    password = pwinput.pwinput(prompt="Mot de passe : ")

    # Vérification du rôle
    role = session.query(Role).filter_by(nom=role_nom).first()
    if not role:
        ErrorMessage.invalid_role()
        return

    # Vérification si l'email existe déjà
    collaborateur = session.query(Collaborateur).filter_by(email=email).first()
    if collaborateur:
        ErrorMessage.account_already_exists()
        return

    # Création du collaborateur
    new_collaborateur = Collaborateur(email=email, password_hash=hash_password(password), nom=nom, role=role)
    session.add(new_collaborateur)
    session.commit()
    SuccessMessage.account_created()

def login():
    delete_token()

    email = input("Email : ")
    password = pwinput.pwinput(prompt="Mot de passe : ")

    collaborateur = session.query(Collaborateur).filter_by(email=email).first()

    if collaborateur and verify_password(password, collaborateur.password_hash.encode('utf-8')):
        token = create_token(collaborateur.id, collaborateur.nom, collaborateur.role.nom)

        save_token(token)
    else:
        ErrorMessage.invalid_credentials()

def login_admin():
    password = ""
    while not password:
        password = pwinput.pwinput(prompt=("Mot de passe (Administrateur): "))
        if not password:
            ErrorMessage.admin_password_empty()
        elif not verify_password(password, ADMIN_PASSWORD):
            ErrorMessage.admin_password_incorrect()
            password = ""


def logout():
    if os.path.exists(TOKEN_PATH) and os.path.getsize(TOKEN_PATH) > 0:
        delete_token()
        SuccessMessage.logout_success()
