from sqlalchemy import create_engine
from models import Base
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_engine(DATABASE_URL)

print("Suppression de toutes les tables existantes...")
Base.metadata.drop_all(engine)
print("Tables supprimées !")

print("Création des nouvelles tables dans la base de données...")
Base.metadata.create_all(engine)
print("Nouvelles tables créées avec succès !")
