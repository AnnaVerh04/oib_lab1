import json


def read_json(path: str) -> dict:
    """
    Читает JSON данные из файла.
        path (str): Путь к файлу JSON.
        dict: JSON данные, загруженные из файла.
    """
    try:
        with open(path, 'r', encoding='UTF-8') as file:
            data = json.load(file)
        return data
    except FileNotFoundError as e:
        print(f"Файл не найден: {e}")
    except Exception as e:
        print(f"При чтении файла произошла ошибка: {str(e)}")


def write_card_numbers_to_json(path: str, keys: list) -> None:
    """
    Записывает список ключей в формате JSON в файл.
        path (str): Путь к файлу, в который будут записаны ключи.
        keys (list): Список ключей для записи.
    """
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
