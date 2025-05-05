from models import Role


class Permission:
    def client_management(role):
        return role == "Commercial"
    
    def contract_management(role):
        return role == "Gestion"
    
    def create_event(role):
        return role == "Commercial"
    
    def assign_event(role):
        return role == "Gestion"
    
    def update_event(role):
        return role in ["Commercial", "Support"]
    
    def delete_event(role):
        return role == "Commercial"