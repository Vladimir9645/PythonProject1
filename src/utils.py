import json
import logging
import os
import re
from typing import Any, Dict, List

# 1. Получаем директорию, где лежит utils.py
current_dir = os.path.dirname(os.path.abspath(__file__))

# 2. Формируем путь к папке logs относительно utils.py (на уровень выше)
log_dir = os.path.join(current_dir, "..", "logs")

# 3. Создаём папку logs, если её нет
os.makedirs(log_dir, exist_ok=True)

# 4. Полный путь к файлу лога
log_file = os.path.join(log_dir, "application.log")

# 5. Настраиваем обработчик логов
json_handler = logging.FileHandler(log_file, encoding="utf-8")
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
json_handler.setFormatter(file_formatter)

# 6. Настройка логгера
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(json_handler)



def dictionary_with_transaction_data(filepath: str) -> List[Dict[str, Any]]:
    """Для обработки выбран JSON-файл."""
    """
    right
    {'id': '4967592.0', 'state': 'EXECUTED', 'date': '2021-11-21T16:57:36Z', 
    'amount': '12868.0', 'currency_name': 'Ruble', 'currency_code': 'RUB', 
    'from': 'Mastercard 4061237171643434', 'to': 'Visa 7539829899017635', 
    'description': 'Перевод с карты на карту'}
    
    json
    [{'id': 441945886, 'state': 'EXECUTED', 'date': '2019-08-26T10:50:58.294041', 
    'operationAmount': {'amount': '31957.58', 'currency': {'name': 'руб.', 'code': 'RUB'}}, 
    'description': 'Перевод организации', 
    'from': 'Maestro 1596837868705199' 'to': 'Счет 64686473678894779589'}
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            data_1 = []
            for transaction in data:
                id_ = transaction.get("id")
                state = transaction.get("state")
                amount = transaction.get("operationAmount", {}).get("amount")
                currency_name = transaction.get("operationAmount", {}).get("currency", {}).get("name")
                currency_name = transaction.get("operationAmount", {}).get("currency", {}).get("code")
                date = transaction.get("date")
                descriptions = transaction.get("descriptions")
                from_ = transaction.get("from")
                to = transaction.get("to")
                data.append({'id': transaction.get("id"),
                             'state': transaction.get("state"),
                             'date': transaction.get("date"),
                             'amount': amount,
                             'currency_name': currency_name,
                             'currency_code': currency_name,
                             'from': transaction.get("from") ,
                             'to': transaction.get("to"),
                             'description': transaction.get("descriptions")})
        return data
    except Exception as e:
        print(f"Ошибка при чтении JSON: {e}")
        return []

def process_bank_search(data: List[Dict[str, Any]], search: str) -> List[Dict[str, Any]]:
    """Ищет операции, где в описании встречается заданная подстрока (без учёта регистра)."""
    if not data or not search:
        return []

    pattern = re.compile(re.escape(search), re.IGNORECASE)
    return [op for op in data if pattern.search(op.get("description", ""))]

#operations = [
 #   {"id": 1, "description": "Перевод 500 руб. другу"},
 #   {"id": 2, "description": "Оплата интернета"},
 #   {"id": 3, "description": "Покупка продуктов на 1000 руб."}
#]

#found = process_bank_search(operations, "500 руб")
# Вернёт: [{"id": 1, "description": "Перевод 500 руб. другу"}]

# Пример вызова функции
if __name__ == "__main__":
    file_path = os.path.join("data", "operations.json")
    transactions = dictionary_with_transaction_data(file_path)

