from models import Role
from .database import DatabaseManager
from messages_managers.error import ErrorMessage
from messages_managers.success import SuccessMessage
from app.settings import ROLES

class RoleManager:
    @staticmethod
    def create_role(db_manager: DatabaseManager):
        role_name = ""

        if not db_manager.check_table_exists(Role.__tablename__):
            return
        
        while role_name not in ROLES:
            print("Choisissez un rôle parmi les suivants :")
            for role in ROLES:
                print(f"- {role}")
            role_name = input("Nom du rôle: ").capitalize()
            if not role_name:
                ErrorMessage.role_empty()
            elif role_name not in ROLES:
                ErrorMessage.invalid_role()

        with db_manager.session_scope() as session:
            role = session.query(Role).filter_by(nom=role_name).first()
            if role:
                ErrorMessage.role_already_exists()
                return

            role = Role(nom=role_name)
            session.add(role)
            session.commit()
            SuccessMessage.role_created(role_name)
