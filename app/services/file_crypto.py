import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def generate_aes_key():
    return AESGCM.generate_key(bit_length=256)

def encrypt_file(data: bytes, key: bytes):
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    encrypted = aesgcm.encrypt(nonce, data, None)
    return nonce + encrypted

def decrypt_file(encrypted_data: bytes, key: bytes):
    aesgcm = AESGCM(key)
    nonce = encrypted_data[:12]
    ciphertext = encrypted_data[12:]
    return aesgcm.decrypt(nonce, ciphertext, None)
