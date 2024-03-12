import binascii
import os
import secrets
from typing import List

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from base64 import urlsafe_b64encode as b64e, urlsafe_b64decode as b64d
import time

from cryptography.hazmat.primitives.twofactor import InvalidToken

backend = default_backend()


def map_data_to_dict(keys: List[str], values: List[str]):
    return dict(zip(keys, values))


def generate_secret_key() -> None:
    import secrets
    print("Onetime Secret Key", secrets.token_bytes(32).hex())


def generate_key_iv():
    iv = os.urandom(12)   # 96-bit IV for GCM
    return iv


def encrypt_password(password: str) -> bytes:
    key: bytes = bytes.fromhex(os.getenv("CIPHER_KEY").strip())
    current_time = int(time.time()).to_bytes(8, 'big')
    algorithm = algorithms.AES(key)
    iv = secrets.token_bytes(algorithm.block_size // 8)
    cipher = Cipher(algorithm, modes.GCM(iv), backend=backend)
    encryptor = cipher.encryptor()
    encryptor.authenticate_additional_data(current_time)
    ciphertext = encryptor.update(password.encode('utf-8')) + encryptor.finalize()
    return b64e(current_time + iv + ciphertext + encryptor.tag)


def decrypt_password(token: bytes) -> bytes:
    key: bytes = bytes.fromhex(os.getenv("CIPHER_KEY").strip())
    algorithm = algorithms.AES(key)
    try:
        data = b64d(token)
    except (TypeError, binascii.Error):
        raise InvalidToken

    timestamp, iv, tag = data[:8], data[8:algorithm.block_size // 8 + 8], data[-16:]
    cipher = Cipher(algorithm, modes.GCM(iv, tag), backend=backend)
    decryptor = cipher.decryptor()
    decryptor.authenticate_additional_data(timestamp)
    ciphertext = data[8 + len(iv):-16]
    return decryptor.update(ciphertext) + decryptor.finalize()

