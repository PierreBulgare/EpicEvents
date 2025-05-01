from models import Role
from .database import DatabaseManager
from .message import MessageManager

class RoleManager:
    def __init__(self, db_manager: DatabaseManager, user):
        self.db_manager = db_manager
        self.user = user

    def create_role(self):
        role_name = ""

        if not self.db_manager.check_table_exists(Role.__tablename__):
            MessageManager.table_not_found(Role.__tablename__)
            return

        while not role_name:
            role_name = input("Nom du role (Commercial, Gestion ou Support): ").capitalize()
            if not role_name:
                MessageManager.role_empty()

        with self.db_manager.session_scope() as session:
            role = session.query(Role).filter_by(nom=role_name).first()
            if role:
                MessageManager.role_already_exists()
                return
            
            role = Role(nom=role_name)
            session.add(role)
            session.commit()
            MessageManager.role_created(role_name)