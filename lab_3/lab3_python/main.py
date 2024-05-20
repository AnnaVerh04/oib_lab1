import argparse
import file_operation
import assymetric
import symmetric
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


ALGORITHMS = ['CAST5', 'RSA']
ENC_OR_DEC = ['encryption', 'decryption']

"""
Модуль для шифрования и дешифрования данных с использованием алгоритмов RSA и CAST5.
Этот модуль содержит функцию main(), которая выполняет шифрование или дешифрование данных в соответствии с переданными параметрами.
"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-alg', '--algorithm', help='Выбор протокола шифрования.', required=True)
    parser.add_argument('-ed', '--enc_or_dec', help='Расшифровка или зашифровка.', required=True)
    # file - из файла, generate - сгенерировать
    # TO DO: добавить ключ, отвечающий за размер ключа при генерации
    parser.add_argument('-k', '--key', help='Откуда берётся ключ при защифровке.')
    parser.add_argument('-s', '--settings', help='Путь к json файлу с путями.', required=True)
    args = parser.parse_args()
    if args.algorithm not in ALGORITHMS:
        print('Название алгоритма введено неверно. Возможные варианты: RSA или CAST5. Завершение работы программы.')
    if args.enc_or_dec not in ENC_OR_DEC:
        print('Ошибка. Возможные варианты: encryption или decryption. Завершение работы программы.')
    if args.key != 'file' and args.key != 'generate' and args.enc_or_dec == 'encryption':
        raise SystemExit

    settings = file_operation.read_json(args.settings)

    if args.enc_or_dec == 'encryption':
        text = file_operation.read_file(settings['text'])
    if args.enc_or_dec == 'decryption':
        text = file_operation.read_bytes_from_file(settings['text'])

    if args.algorithm == 'RSA':
        RSA = assymetric.RSA()
        if args.enc_or_dec == 'encryption':
            if args.key == 'file':
                RSA.get_open_key_from_file(settings['rsa_public_key'])
            if args.key == 'generate':
                RSA.generate_key()
                RSA.get_key_to_file(settings['rsa_public_key'], settings['rsa_private_key'])
            bytes_ = bytes(text, 'UTF-8')
            c_text = RSA.encrypt_bytes(bytes_)
            file_operation.write_bytes_to_file(settings['text_after_encryption_rsa'], c_text)

        if args.enc_or_dec == 'decryption':
            RSA.get_private_key_from_file(settings['rsa_private_key'])
            cc_text = RSA.decrypt_bytes(text).decode('UTF-8')
            file_operation.write_file(settings['text_after_decryption_rsa'], cc_text)

    if args.algorithm == 'CAST5':
        CAST5 = symmetric.CAST_5()
        if args.enc_or_dec == 'encryption':
            if args.key == 'file':
                CAST5.get_key_from_file(settings['CAST5_key'])
            if args.key == 'generate':
                CAST5.generate_key()
                CAST5.get_key_to_file(settings['CAST5_key'])
            bytes_ = bytes(text, 'UTF-8')
            c_text = CAST5.encrypt_bytes(bytes_)
            file_operation.write_bytes_to_file(settings['text_after_encryption_cast5'], c_text)
        if args.enc_or_dec == 'decryption':
            CAST5.get_key_from_file(settings['CAST5_key'])
            cc_text = CAST5.decrypt_bytes(text).decode('UTF-8', errors='ignore')
            file_operation.write_file(settings['text_after_decryption_cast5'], cc_text)


if __name__ == '__main__':
    main()