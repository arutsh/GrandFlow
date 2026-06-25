import base64
import os

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

_NONCE_SIZE = 12


def encrypt(plaintext: str, key_b64: str) -> str:
    key = base64.b64decode(key_b64)
    nonce = os.urandom(_NONCE_SIZE)
    ciphertext = AESGCM(key).encrypt(nonce, plaintext.encode(), None)
    return base64.b64encode(nonce + ciphertext).decode()


def decrypt(ciphertext_b64: str, key_b64: str) -> str:
    key = base64.b64decode(key_b64)
    data = base64.b64decode(ciphertext_b64)
    nonce, ciphertext = data[:_NONCE_SIZE], data[_NONCE_SIZE:]
    return AESGCM(key).decrypt(nonce, ciphertext, None).decode()
