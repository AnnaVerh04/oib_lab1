import json


# json в словарь
def read_json(path: str) -> dict:
    try:
        with open(path, 'r', encoding='UTF-8') as file:
            data = json.load(file)
        return data
    except FileNotFoundError as e:
        print(f"Файл не найден: {e}")
    except Exception as e:
        print(f"При чтении файла произошла ошибка: {str(e)}")


def write_card_numbers_to_json(path, keys):
    try:
        with open(path, "w", encoding='UTF-8') as file:
            file.write('{\n\t"keys": [')
            for i in range(len(keys) - 1):
                file.write(keys[i])
                file.write(', ')
            file.write(keys[-1])
            file.write(']\n}')
    except Exception as e:
        print(f"Произошла ошибка при работе с файлом {file}: {e}")
