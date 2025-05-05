from models import Collaborateur, Role
from messages_managers.error import ErrorMessage
from messages_managers.warning import WarningMessage
from .database import DatabaseManager
from .user import UserManager
from utils.utils import Utils


class CollaborateurManager:
    def __init__(self, db_manager: DatabaseManager, user: UserManager):
        self.db_manager = db_manager
        self.user = user

    @staticmethod
    def get_collaborateur(session, warning=False):
        if warning:
            WarningMessage.cancel_command_info()

        while True:
            try:
                email = input("Email du collaborateur : ")
                if not email:
                    ErrorMessage.client_name_empty()
                    continue
                if not Utils.email_is_valid(email):
                    ErrorMessage.invalid_email()
                    continue
                collab = session.query(Collaborateur
                                        ).filter_by(email=email
                                                    ).first()
                if not collab:
                    ErrorMessage.data_not_found("Collaborateur", email)
                    continue
                return collab
            except KeyboardInterrupt:
                WarningMessage.action_cancelled()
                return