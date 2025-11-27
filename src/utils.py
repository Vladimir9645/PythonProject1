import json
import os
from typing import Any, Dict, List


def dictionary_with_transaction_data(file_path: str = os.path.join('data', 'operations.json')) -> (List)[Dict[str, Any]]:
    """
    Загружает данные из файла и возвращает их списком операций.
    Если файл отсутствует,
    пустой или содержит некорректный JSON,
    возвращает пустой список.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if isinstance(data, list):
                return data
            else:
                return []
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Вызов функции с правильным аргументом
file_path = os.path.join('data', 'operations.json')
transactions = dictionary_with_transaction_data(file_path)
print(transactions)
