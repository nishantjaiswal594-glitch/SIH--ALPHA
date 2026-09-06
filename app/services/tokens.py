import hashlib
import secrets
from datetime import datetime, timedelta


def generate_token():
    return secrets.token_urlsafe(32)


def hash_token(token: str):
    return hashlib.sha256(
        token.encode("utf-8")
    ).hexdigest()


def token_expiry():
    return datetime.utcnow() + timedelta(minutes=30)