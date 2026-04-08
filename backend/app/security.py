"""Token encryption utilities.

GitHub access tokens are encrypted at rest using Fernet symmetric encryption.
The Fernet key is derived from SECRET_KEY so no separate key management is needed.
"""
import base64
import hashlib

from cryptography.fernet import Fernet


def _fernet(secret_key: str) -> Fernet:
    # Derive a 32-byte key from SECRET_KEY using SHA-256
    key_bytes = hashlib.sha256(secret_key.encode()).digest()
    fernet_key = base64.urlsafe_b64encode(key_bytes)
    return Fernet(fernet_key)


def encrypt_token(token: str, secret_key: str) -> str:
    return _fernet(secret_key).encrypt(token.encode()).decode()


def decrypt_token(encrypted: str, secret_key: str) -> str:
    return _fernet(secret_key).decrypt(encrypted.encode()).decode()
