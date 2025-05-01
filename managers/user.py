
class UserManager:
    def __init__(self):
        pass

    def init_user(self, token, payload):
        self.id = payload.get("user_id")
        self.name = payload.get("user_name")
        self.role = payload.get("user_role")
        self.token = token
        self.payload = payload