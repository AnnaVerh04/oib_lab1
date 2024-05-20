import json


def read_json(path: str) -> dict:
    """
        Читает данные из JSON-файла и возвращает содержимое в виде словаря.
        path (str)- Путь к JSON-файлу для чтения.
        dict - Содержимое JSON-файла в виде словаря.
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
       path (str) - Путь к файлу, в который нужно записать данные.
       data (str) - Строка данных для записи в файл.
    """
    try:
        with open(path, "a+", encoding='UTF-8') as file:
            file.write(data)
    except FileNotFoundError:
        print(f"Создан файл с названием: {path}")
    except Exception as e:
        print(f"Произошла ошибка при работе с файлом {path}: {e}")


def read_file(pathname: str) -> str:
    """
       Читает данные из файла и возвращает их в виде строки.
       pathname (str) - Путь к файлу для чтения.
       str - Содержимое файла в виде строки.
    """
    s = ''
    try:
        with open(pathname, 'r', encoding='utf-8') as file_read:
            s = file_read.read()
    except FileNotFoundError as e:
        print(f"Файл не найден: {e}")
    return s


def write_bytes_to_file(path, bytes_) -> None:
    """
       Записывает байтовые данные в файл.
       path (str) - Путь к файлу, в который нужно записать байтовые данные.
       bytes_ (bytes) - Байтовые данные для записи в файл.
       """
    try:
        with open(path, "wb") as file:
            file.write(bytes_)
    except FileNotFoundError:
        print(f"Создан файл с названием: {path}")
    except Exception as e:
        print(f"Произошла ошибка при работе с файлом {path}: {e}")


def read_bytes_from_file(pathname) -> bytes:
    """
        Читает байтовые данные из файла и возвращает их.
        pathname (str): Путь к файлу для чтения.
        bytes: Байтовые данные из файла.
        """
    s = ''
    try:
        with open(pathname, 'rb') as file_read:
            s = file_read.read()
    except FileNotFoundError as e:
        print(f"Файл не найден: {e}")
    return s



