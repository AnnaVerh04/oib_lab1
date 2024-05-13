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
        padder = padding.ANSIX923(32).padder()
        padded_bytes = padder.update(bytes_) + padder.finalize()

        iv = os.urandom(8)
        cipher = Cipher(algorithms.CAST5(self.key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        c_bytes = encryptor.update(padded_bytes) + encryptor.finalize()
        return c_bytes, cipher, iv

    def decrypt_bytes(self, bytes_, cipher):
        decryptor = cipher.decryptor()
        res = decryptor.update(bytes_) + decryptor.finalize()
        unpadder = padding.ANSIX923(32).unpadder()
        unpadded_bytes = unpadder.update(res) + unpadder.finalize()
        return unpadded_bytes


if __name__ == '__main__':
    """
    cyp = CAST_5()
    cyp.generate_key()
    s = bytes('Very rainy day', 'UTF-8')
    enc, cipher, iv = cyp.encrypt_bytes(s)
    cipher2 = Cipher(algorithms.CAST5(cyp.key), modes.CBC(iv))
    dec = cyp.decrypt_bytes(enc, cipher2)
    print(dec.decode('UTF-8'))
    """

    import file_operation

    """
    s = bytes('Very rainy day', 'UTF-8')
    cyp = CAST_5()
    cyp.generate_key()
    enc, cypher, iv = cyp.encrypt_bytes(s)
    file_operations.write_bytes_to_file('enc.txt', enc)
    file_operations.write_bytes_to_file('iv.txt', iv)
    cyp.get_key_to_file('key.txt')
    """
    enc = file_operation.read_bytes_from_file('enc.txt')
    iv = file_operation.read_bytes_from_file('iv.txt')
    cyp = CAST_5()
    cyp.get_key_from_file('key.txt')
    cypher = Cipher(algorithms.CAST5(cyp.key), modes.CBC(iv))
    print(cyp.decrypt_bytes(enc, cypher).decode('UTF-8'))
