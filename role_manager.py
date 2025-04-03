from jwt_utils import verifier_role
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Chargement de l'environnement
load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

# Connexion à la base de données
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

TOKEN_PATH = os.path.join(os.path.dirname(__file__), ".token")


def get_user_role(user):
    with open(TOKEN_PATH, "r") as f:
        token = f.read().strip()