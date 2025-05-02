from models import Role
from .database import DatabaseManager
from .message import MessageManager
from settings import ROLES


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
                MessageManager.role_empty()
            elif role_name not in ROLES:
                MessageManager.invalid_role()

        with db_manager.session_scope() as session:
            role = session.query(Role).filter_by(nom=role_name).first()
            if role:
                MessageManager.role_already_exists()
                return

            role = Role(nom=role_name)
            session.add(role)
            session.commit()
            MessageManager.role_created(role_name)
