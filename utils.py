import json

def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return "Файл не найден."
    except IOError:
        return "Ошибка при чтении файла."


def string_to_json(json_string):
    try:
        json_object = json.loads(json_string)
        return json_object
    except json.JSONDecodeError:
        return "Ошибка: строка не является корректным JSON."