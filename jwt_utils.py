import jwt
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "default_secret")

# Générer un token JWT
def creer_token(user_id, user_role, expire_minutes=60):
    payload = {
        "user_id": user_id,
        "user_role": user_role,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=expire_minutes),
        "iat": datetime.now(timezone.utc)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

# Vérifier et décoder un token JWT
def verifier_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token expiré
    except jwt.InvalidTokenError:
        return None  # Token invalide
    
# Vérifier le rôle d'un utilisateur
def verifier_role(token, role):
    payload = verifier_token(token)
    if payload and payload.get("user_role") == role:
        return True
    return False
