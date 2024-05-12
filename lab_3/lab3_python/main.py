import argparse
import assymetric

# Способ шифрования: CAST5, RSA
# Способ ввода ключа: из файла, сгенерировать программой (в этом случае ввод длины ключа)
# Способ ввода текста для шифровки: из файла, с клавиатуры
# Способ ввода текста (байтов) для расшифровки: из файла, с клавиатуры
# Способ сохранения: в файл,

ALGORITHMS = ['CAST5', 'RSA']
ENC_OR_DEC = ['encryption', 'decryption']


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-alg', '--algorithm', help='Выбор протокола шифрования.', required=True)
    parser.add_argument('-ed', '-enc_or_dec', help='Расшифровка или зашифровка.', required=True)
    parser.add_argument('-s', '--settings', help='Путь к json файлу с путями.', required=True)
    args = parser.parse_args()
    if args.algorithm not in ALGORITHMS:
        print('Название алгоритма введено неверно. Возможные варианты: RSA или CAST5. Завершение работы программы.')
    if args.enc_or_dec not in ENC_OR_DEC:
        print('Ошибка. Возможные варианты: encryption или decryption. Завершение работы программы.')

    settings = {}  # Словарь, которые составлен из settings.json

    # Считывание текста из файла
    with open(settings['text'], 'rb') as t:
        text = t.read()
    #

    if args.algorithm == 'RSA':
        RSA = assymetric.RSA()
        RSA.get_keys_from_file(settings['rsa_public_key'], settings['rsa_private_key'])
        if args.enc_or_dec == 'encryption':
            bytes_ = bytes(text, 'UTF-8')
            c_text = RSA.encrypt_bytes(bytes_)
        else:
            dc_text = RSA.decrypt_bytes(text)
            c_text = dc_text.decode('UTF-8')

        # Сохранение текста в файл
        with open(settings['text_after']) as t:
            t.write(c_text)
        #


if __name__ == '__main__':
    main()