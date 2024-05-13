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


# запись в файл
def write_file(path: str, data: str) -> None:
    try:
        with open(path, "a+", encoding='UTF-8') as file:
            file.write(data)
    except FileNotFoundError:
        print(f"Создан файл с названием: {path}")
    except Exception as e:
        print(f"Произошла ошибка при работе с файлом {path}: {e}")


# чтение из файла
def read_file(pathname: str) -> str:
    s = ''
    try:
        with open(pathname, 'r', encoding='utf-8') as file_read:
            s = file_read.read()
    except FileNotFoundError as e:
        print(f"Файл не найден: {e}")
    return s


# запись байтов в файл
def write_bytes_to_file(path, bytes_):
    try:
        with open(path, "wb") as file:
            file.write(bytes_)
    except FileNotFoundError:
        print(f"Создан файл с названием: {path}")
    except Exception as e:
        print(f"Произошла ошибка при работе с файлом {path}: {e}")


# считывание байтов из файла
def read_bytes_from_file(pathname):
    s = ''
    try:
        with open(pathname, 'rb') as file_read:
            s = file_read.read()
    except FileNotFoundError as e:
        print(f"Файл не найден: {e}")
    return s


if __name__ == '__main__':
    pass
