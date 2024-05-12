from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_pem_private_key


class RSA:
    def __init__(self):
        # Последовательности байтов
        self.public_key = None
        self.private_key = None

    def generate_keys(self, public_exponent=65537, key_size=2048):
        keys = rsa.generate_private_key(
            public_exponent=public_exponent,
            key_size=key_size
        )
        self.public_key = keys.public_key()
        self.private_key = keys

    def get_key_to_file(self, path_public, path_private):
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

    def get_keys_from_file(self, path_public, path_private):
        with open(path_public, 'rb') as pem_in:
            public_bytes = pem_in.read()
        self.public_key = load_pem_public_key(public_bytes)
        with open(path_private, 'rb') as pem_in:
            private_bytes = pem_in.read()
        self.private_key = load_pem_private_key(private_bytes, password=None)

    def encrypt_bytes(self, bytes_):
        enc_bytes = self.public_key.encrypt(bytes_, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                                                 algorithm=hashes.SHA256(), label=None))
        return enc_bytes

    def decrypt_bytes(self, bytes_):
        dec_bytes = self.private_key.decrypt(bytes_, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                                                  algorithm=hashes.SHA256(), label=None))
        return dec_bytes


if __name__ == '__main__':
    """
    a = RSA()
    a.generate_keys()
    a.get_key_to_file('public.txt', 'private.txt')
    a.get_keys_from_file('public.txt', 'private.txt')
    text = ''
    b = bytes(text, 'UTF-8')
    enc = a.encrypt_bytes(b)
    dec = a.decrypt_bytes(enc)
    print(dec.decode('UTF-8'))
    """
