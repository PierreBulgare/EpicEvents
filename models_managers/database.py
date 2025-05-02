from app.settings import DATABASE_URL
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager
from models import Base
from messages_managers.success import SuccessMessage
from messages_managers.error import ErrorMessage
from messages_managers.warning import WarningMessage

class DatabaseManager:
    def __init__(self):
        self.engine = sqlalchemy.create_engine(DATABASE_URL)
        self.Session = sessionmaker(bind=self.engine, autoflush=False, expire_on_commit=False)

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
        try:
            session.close()
        except SQLAlchemyError as e:
            ErrorMessage.session_close_error(e)

    def drop_all(self):
        """
        Supprime toutes les tables de la base de données.
        """
        Base.metadata.drop_all(self.engine)
        SuccessMessage.tables_dropped()

    def create_all(self):
        """
        Crée et met à jour toutes les tables de la base de données.
        """
        inspector = sqlalchemy.inspect(self.engine)
        existing_tables = inspector.get_table_names()
        table_updated = 0
        for table_name, table in Base.metadata.tables.items():
            if table_name not in existing_tables:
                Base.metadata.create_all(self.engine, tables=[table])
                SuccessMessage.table_created(table_name)
                table_updated += 1
            else:
                existing_columns = [col['name'] for col in inspector.get_columns(table_name)]
                for column in table.columns:
                    if column.name not in existing_columns:
                        with self.engine.begin() as connection:
                            sql = f'ALTER TABLE {table_name} ADD COLUMN {column.name} {column.type.compile(dialect=self.engine.dialect)}'
                            connection.execute(sqlalchemy.text(sql))
                            SuccessMessage.column_added(table_name, column.name)
                            table_updated += 1
        if table_updated == 0:
            WarningMessage.no_table_update()

    def check_table_exists(self, table_name):
        """
        Vérifie si une table existe dans la base de données.
        """
        inspector = sqlalchemy.inspect(self.engine)
        exist = inspector.has_table(table_name)
        if not exist:
            ErrorMessage.table_not_found(table_name)
            return False
        return True

    @contextmanager
    def session_scope(self):
        session = self.get_session()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Erreur : {e}")
        finally:
            self.close_session(session)