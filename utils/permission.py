from models import Role


class Permission:
    @staticmethod
    def client_management(role):
        return role == "Commercial"
    
    @staticmethod
    def contract_management(role):
        return role in ["Gestion", "Commercial"]

    @staticmethod
    def sign_contract(role):
        return role == "Commercial"
    
    @staticmethod
    def collab_management(role):
        return role == "Gestion"
    
    @staticmethod
    def create_event(role):
        return role == "Commercial"
    
    @staticmethod
    def assign_event(role):
        return role == "Gestion"
    
    @staticmethod
    def update_event(role):
        return role in ["Commercial", "Support"]
    
    @staticmethod
    def delete_event(role):
        return role == "Commercial"