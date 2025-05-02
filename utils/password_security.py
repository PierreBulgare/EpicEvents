import bcrypt


class PasswordSecurity:
    @staticmethod
    def hash(password: str) -> str:
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return hashed.decode('utf-8')

    @staticmethod
    def verify(password: str, hashed_password: str) -> bool:
        if isinstance(hashed_password, str):
            hashed_password = hashed_password.encode('utf-8')
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
