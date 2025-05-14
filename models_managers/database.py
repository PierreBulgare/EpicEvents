from app.settings import DATABASE_URL
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager
from models import Base
from messages_managers.success import SuccessMessage
from messages_managers.error import ErrorMessage
from messages_managers.warning import WarningMessage
from utils.utils import Utils
from messages_managers.text import TextManager
from datetime import datetime


class DatabaseManager:
    def __init__(self):
        self.engine = sqlalchemy.create_engine(DATABASE_URL)
        self.Session = sessionmaker(
            bind=self.engine,
            autoflush=False,
            expire_on_commit=False)

    def get_engine(self):
        """
        Retourne l'instance du moteur SQLAlchemy.
        """
        return self.engine

    def get_session(self):
        """
        Retourne une nouvelle session SQLAlchemy.
        """
        return self.Session()

    def close_session(self, session):
        """
        Ferme proprement la session SQLAlchemy.
        """
        try:
            session.close()
        except SQLAlchemyError as e:
            ErrorMessage.session_close_error(e)

    def drop_all(self, confirm=True):
        """
        Supprime toutes les tables de la base de données.
        """
        if confirm:
            choices = ["Confirmer", "Annuler"]
            print(
                TextManager.color(
                    "ATTENTION : Cette action supprimera"
                    "toutes les tables de la base de données !",
                    "yellow"))
            while True:
                answer = Utils.get_questionnary(choices)
                match answer:
                    case "Confirmer":
                        break
                    case "Annuler":
                        WarningMessage.action_cancelled()
                        return
                    case _:
                        ErrorMessage.action_not_recognized()

        Base.metadata.drop_all(self.engine)
        SuccessMessage.tables_dropped()

    def create_all(self):
        """
        Crée et met à jour toutes les tables de la base de données.
        """
        # Création directe de toutes les tables
        Base.metadata.create_all(self.engine)
        for table_name, table in Base.metadata.tables.items():
            SuccessMessage.table_created(table_name)

        # Mise à jour des colonnes manquantes
        inspector = sqlalchemy.inspect(self.engine)
        for table_name, table in Base.metadata.tables.items():
            if inspector.has_table(table_name):
                existing_columns = [col['name']
                                    for col in inspector.get_columns(
                                        table_name)]
                for column in table.columns:
                    if column.name not in existing_columns:
                        column_type = column.type.compile(
                            dialect=self.engine.dialect)
                        sql = f'ALTER TABLE {table_name} ADD COLUMN {
                            column.name} {column_type}'

                        with self.engine.begin() as connection:
                            connection.execute(sqlalchemy.text(sql))
                            SuccessMessage.column_added(
                                table_name, column.name)

    def check_table_exists(self, table_name):
        """
        Vérifie si une table existe dans la base de données.
        """
        inspector = sqlalchemy.inspect(self.engine)
        exist = inspector.has_table(table_name)
        return exist

    @contextmanager
    def session_scope(self):
        """
        Contexte sécurisé pour une session SQLAlchemy.
        """
        session = self.get_session()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Erreur : {e}")
        finally:
            self.close_session(session)

    def update_commit(self, model, session):
        """
        Commit les changements dans la session.
        """
        model.derniere_maj = datetime.now()
        session.commit()
