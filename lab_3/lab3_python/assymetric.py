from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_pem_private_key


class RSA:
    def __init__(self):
        """
           Класс, представляющий объект RSA для работы с открытым и закрытым ключами.
           public_key: Открытый ключ RSA.
           private_key: Закрытый ключ RSA.
        """
        self.public_key = None
        self.private_key = None

    def generate_key(self, key_size=2048) -> None:
        """
           Генерирует открытый и закрытый ключи RSA заданного размера.
           key_size (int) - Размер ключа RSA.
        """
        keys = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_size
        )
        self.public_key = keys.public_key()
        self.private_key = keys

    def get_key_to_file(self, path_public, path_private) -> None:
        """
           Сохраняет открытый и закрытый ключи RSA в файлы.
           path_public (str) - Путь к файлу для сохранения открытого ключа.
           path_private (str) -  Путь к файлу для сохранения закрытого ключа.
        """
        if self.public_key is None:
            print('Ключи ещё не сгенерированы.')
            return
        with open(path_public, 'wb') as public_out:
            public_out.write(self.public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                                          format=serialization.PublicFormat.SubjectPublicKeyInfo))
        with open(path_private, 'wb') as private_out:
            private_out.write(self.private_key.private_bytes(encoding=serialization.Encoding.PEM,
                                                             format=serialization.PrivateFormat.TraditionalOpenSSL,
                                                             encryption_algorithm=serialization.NoEncryption()))

    def get_open_key_from_file(self, path_public) -> None:
        """
            Загружает открытый ключ RSA из файла.
            path_public (str) - Путь к файлу с открытым ключом.
        """
        with open(path_public, 'rb') as pem_in:
            public_bytes = pem_in.read()
        self.public_key = load_pem_public_key(public_bytes)

    def get_private_key_from_file(self, path_private) -> None:
        """
            Загружает закрытый ключ RSA из файла.
            path_private (str) - Путь к файлу с закрытым ключом.
        """
        with open(path_private, 'rb') as pem_in:
            private_bytes = pem_in.read()
        self.private_key = load_pem_private_key(private_bytes, password=None)

    def encrypt_bytes(self, bytes_: bytes) -> bytes:
        """
            Шифрует байтовые данные с использованием открытого ключа RSA.
            bytes_(bytes) -  Байтовые данные для шифрования.
            bytes - Зашифрованные байтовые данные.
         """
        enc_bytes = self.public_key.encrypt(bytes_, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                                                 algorithm=hashes.SHA256(), label=None))
        return enc_bytes

    def decrypt_bytes(self, bytes_: bytes) -> bytes:
        """
            Расшифровывает байтовые данные с использованием закрытого ключа RSA.
            bytes_ (bytes) - Зашифрованные байтовые данные для расшифровки.
            bytes - Расшифрованные байтовые данные.
        """
        dec_bytes = self.private_key.decrypt(bytes_, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                                                  algorithm=hashes.SHA256(), label=None))
        return dec_bytes
