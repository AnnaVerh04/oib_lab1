import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding


class CAST_5:
    def __init__(self, key=None):
        """
            Класс, представляющий алгоритм CAST-5 для шифрования данных.
            key - Ключ для шифрования данных.
        """
        self.key = key

    def generate_key(self, key_size=16) -> None:
        """
            Генерирует случайный ключ заданного размера и сохраняет его в атрибут key.
            key_size (int) - Размер ключа в байтах (по умолчанию 16).
        """
        self.key = os.urandom(key_size)

    def get_key_to_file(self, path: str) -> None:
        """
            Сохраняет ключ в файл.
            path (str) - Путь к файлу для сохранения ключа.
         """
        with open(path, 'wb') as key_file:
            key_file.write(self.key)

    def get_key_from_file(self, path: str) -> None:
        """
            Загружает ключ из файла.
            path (str): Путь к файлу с ключом.
        """
        with open(path, 'rb') as key_file:
            self.key = key_file.read()

    def encrypt_bytes(self, bytes_: bytes) -> bytes:
        """
            Шифрует байтовые данные с использованием алгоритма CAST-5.
            bytes_ (bytes): Байтовые данные для шифрования.
            bytes: Зашифрованные байтовые данные.
        """
        padder = padding.ANSIX923(128).padder()
        padded_bytes = padder.update(bytes_) + padder.finalize()

        iv = os.urandom(8)
        cipher = Cipher(algorithms.CAST5(self.key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        c_bytes = encryptor.update(padded_bytes) + encryptor.finalize()
        return c_bytes

    def decrypt_bytes(self, bytes_: bytes) -> bytes:
        """
               Расшифровывает байтовые данные, зашифрованные алгоритмом CAST-5.
               bytes_ (bytes): Зашифрованные байтовые данные для расшифровки.
               bytes: Расшифрованные байтовые данные.
        """
        iv = os.urandom(8)
        cipher = Cipher(algorithms.CAST5(self.key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        res = decryptor.update(bytes_) + decryptor.finalize()
        unpadder = padding.ANSIX923(128).unpadder()
        unpadded_bytes = unpadder.update(res) + unpadder.finalize()
        return unpadded_bytes


