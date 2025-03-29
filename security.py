import bcrypt

# Hasher un mot de passe (enregistrer sous forme utf-8)
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

# Vérifier un mot de passe (convertir en bytes avant vérification)
def verify_password(password: str, hashed) -> bool:
    if isinstance(hashed, str):
        hashed = hashed.encode('utf-8')  # encodage uniquement si c'est une string
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

