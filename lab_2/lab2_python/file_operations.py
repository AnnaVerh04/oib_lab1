import json


def read_json(path: str) -> dict:
    """
       Читает данные из JSON-файла и возвращает содержимое в виде словаря.
       Параметры:
       path (str): Путь к JSON-файлу для чтения.
       Возвращает:
       dict: Содержимое JSON-файла в виде словаря.
       """
    try:
        with open(path, 'r', encoding='UTF-8') as file:
            data = json.load(file)
        return data
    except FileNotFoundError as e:
        print(f"Файл не найден: {e}")
    except Exception as e:
        print(f"При чтении файла произошла ошибка: {str(e)}")


def write_file(path: str, data: str) -> None:
    """
       Записывает данные в файл.
       Параметры:
       path (str): Путь к файлу, в который нужно записать данные.
       data (str): Строка данных для записи в файл.
       Возвращает:
       None
       """
    try:
        with open(path, "a+", encoding='UTF-8') as file:
            file.write(data)
        print(f"The data has been successfully written to the file '{path}'.")
    except Exception as e:
        print(f"An error occurred while writing the file: {str(e)}")