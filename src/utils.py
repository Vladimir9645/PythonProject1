import json
import os


def dictionary_with_transaction_data()-> list:
    """
    Загружает данные из файла operations.json и
    возвращает их списком операций.

    Если файл отсутствует, пустой или содержит некорректный JSON,
    возвращает пустой список.
    """

    # Путь до текущего скрипта
    script_dir = os.path.dirname(__file__)
    # Путь до файла operations.json
    file_path = os.path.join(script_dir, "data", "operations.json")

    if not os.path.exists(file_path):
        return []  # Файл не найден — пустой список

    try:
        with open(file_path, encoding="utf-8") as json_file:
            data = json.load(json_file)
            if isinstance(data, list):  # Проверка, что данные — список
                return data  # Возвращаем список операций
            else:
                return []  # Если не список — пустой список
    except (json.JSONDecodeError, UnicodeDecodeError):
        return []  # Ошибка при чтении JSON — пустой список


# Пример вызова:
operations = dictionary_with_transaction_data()
print(operations)  # Выводит список операций
