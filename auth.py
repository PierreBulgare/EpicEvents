import os
import sentry_sdk
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pwinput

from models import Collaborateur, Role
from security import verify_password, hash_password
from jwt_utils import create_token, delete_token, save_token
from managers.error_message import ErrorMessage
from managers.success_message import SuccessMessage
from managers.warning_message import WarningMessage
from settings import ADMIN_PASSWORD

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()
TOKEN_PATH = os.path.join(os.path.dirname(__file__), ".token")


def create_account():
    """
    Crée un compte collaborateur.
    """
    delete_token()
    WarningMessage.cancel_command_info()

    # Prénom
    while True:
        prenom = input("Prénom : ")
        if not prenom:
            ErrorMessage.user_firstname_empty()
            continue
        break

    # Nom
    while True:
        nom_de_famille = input("Nom : ")
        if not nom_de_famille:
            ErrorMessage.username_empty()
            continue
        nom = prenom + " " + nom_de_famille.upper()
        break

    # Email
    while True:
        email = input("Email : ")
        if not email:
            ErrorMessage.email_empty()
            continue
        if "@" not in email or "." not in email.split("@")[-1]:
            ErrorMessage.invalid_email()
            continue
        try:
            collaborateur = session.query(Collaborateur).filter_by(email=email).first()
        except Exception as e:
            ErrorMessage.database_error()
            sentry_sdk.capture_exception(e)
            continue
        if collaborateur:
            ErrorMessage.account_already_exists()
            continue
        break

    # Rôle
    while True:
        role_nom = input("Rôle (Commercial, Gestion, Support) : ").capitalize()
        if not role_nom:
            ErrorMessage.role_empty()
            continue
        try:
            role = session.query(Role).filter_by(nom=role_nom).first()
        except Exception as e:
            ErrorMessage.database_error()
            sentry_sdk.capture_exception(e)
            continue
        if not role:
            ErrorMessage.invalid_role()
            continue
        break

    # Mot de passe
    while True:
        password = pwinput.pwinput(prompt="Mot de passe : ")
        if not password:
            ErrorMessage.password_empty()
            continue
        if len(password) < 8:
            ErrorMessage.password_too_short()
            continue
        break

    # Création du collaborateur
    new_collaborateur = Collaborateur(
        email=email,
        password_hash=hash_password(password),
        nom=nom,
        role=role
    )
    session.add(new_collaborateur)
    session.commit()
    SuccessMessage.account_created()


def login():
    delete_token()

    email = input("Email : ")
    password = pwinput.pwinput(prompt="Mot de passe : ")

    try:
        collaborateur = session.query(Collaborateur).filter_by(email=email).first()
    except Exception as e:
        ErrorMessage.database_error()
        sentry_sdk.capture_exception(e)
        return

    if (collaborateur 
        and verify_password(
            password, collaborateur.password_hash.encode('utf-8')
            )):
        token = create_token(
            collaborateur.id,
            collaborateur.nom,
            collaborateur.role.nom
        )
        save_token(token)
    else:
        ErrorMessage.invalid_credentials()


def login_admin():
    password = ""
    while not password:
        password = pwinput.pwinput(prompt="Mot de passe (Administrateur): ")
        if not password:
            ErrorMessage.admin_password_empty()
        elif not verify_password(password, ADMIN_PASSWORD):
            ErrorMessage.admin_password_incorrect()
            password = ""


def logout():
    if os.path.exists(TOKEN_PATH) and os.path.getsize(TOKEN_PATH) > 0:
        delete_token()
        SuccessMessage.logout_success()
