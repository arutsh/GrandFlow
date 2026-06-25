import base64
import pytest
from cryptography.exceptions import InvalidTag

from app.utils.encryption import encrypt, decrypt


def _make_key() -> str:
    import secrets
    return base64.b64encode(secrets.token_bytes(32)).decode()


class TestEncryption:
    def test_round_trip(self):
        key = _make_key()
        plaintext = "sk-ant-api03-supersecretkey"
        assert decrypt(encrypt(plaintext, key), key) == plaintext

    def test_different_ciphertexts_for_same_plaintext(self):
        key = _make_key()
        plaintext = "same-input"
        assert encrypt(plaintext, key) != encrypt(plaintext, key)

    def test_wrong_key_raises(self):
        key1 = _make_key()
        key2 = _make_key()
        ciphertext = encrypt("secret", key1)
        with pytest.raises((InvalidTag, Exception)):
            decrypt(ciphertext, key2)

    def test_tampered_ciphertext_raises(self):
        key = _make_key()
        ciphertext_b64 = encrypt("secret", key)
        raw = bytearray(base64.b64decode(ciphertext_b64))
        raw[-1] ^= 0xFF
        tampered = base64.b64encode(bytes(raw)).decode()
        with pytest.raises((InvalidTag, Exception)):
            decrypt(tampered, key)
