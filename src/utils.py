import json
import os


def dictionary_with_transaction_data():
    """
    Загружает данные из файла operations.json и
    возвращает их списком операций.
    Если файл отсутствует,
    пустой или содержит некорректный JSON,
    возвращает пустой список.
    """

    # Собираем путь к файлу
    patch = os.path.join('data', 'operations.json')

    try:
        with open(patch, 'r', encoding='utf-8') as file:
            data = json.load(file)
            # Предполагаем, что это список операций
            if isinstance(data, list):
                return data
            else:
                return []
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Пример вызова функции
transactions = dictionary_with_transaction_data()
print(transactions)
