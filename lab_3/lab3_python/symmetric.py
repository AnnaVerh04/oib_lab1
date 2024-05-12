import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding


class CAST_5:
    def __init__(self, key=None):
        self.key = key

    def generate_key(self, key_size=16):
        self.key = os.urandom(key_size)

    def get_key_to_file(self, path):
        with open(path, 'wb') as key_file:
            key_file.write(self.key)

    def get_key_from_file(self, path):
        with open(path, 'rb') as key_file:
            self.key = key_file.read()

    def encrypt_bytes(self, bytes_):
        iv = os.urandom(8)
        cipher = Cipher(algorithms.CAST5(self.key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        c_text = encryptor.update(bytes_)
        return c_text, cipher

    def decrypt_bytes(self, bytes_, cipher):
        decryptor = cipher.decryptor()
        res = decryptor.update(bytes_) + decryptor.finalize()
        return res
