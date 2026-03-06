from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey, Ed25519PublicKey
)
import jwt, datetime, os

SECRET_KEY = os.getenv("SECRET_KEY", "supersecret")
ALGORITHM = "HS256"

def generate_keypair():
    private_key = Ed25519PrivateKey.generate()
    public_key = private_key.public_key()

    private_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption()
    )

    public_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw
    )

    return private_bytes, public_bytes


def sign_data(private_key_bytes: bytes, data: bytes) -> bytes:
    private_key = Ed25519PrivateKey.from_private_bytes(private_key_bytes)
    return private_key.sign(data)


def verify_signature(public_key_bytes: bytes, data: bytes, signature: bytes) -> bool:
    try:
        public_key = Ed25519PublicKey.from_public_bytes(public_key_bytes)
        public_key.verify(signature, data)
        return True
    except Exception:
        return False


def create_access_token(data: dict):
    payload = data.copy()
    payload["exp"] = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
