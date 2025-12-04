import json
import os
import logging
from typing import Any, Dict, List

# Создаём отдельный логгер для модуля utils
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # уровень логирования не ниже DEBUG

# Настраиваем файловый хендлер
file_handler = logging.FileHandler('../logs/application.log', encoding='utf-8')
file_formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def dictionary_with_transaction_data(
    file_path: str = os.path.join("data", "operations.json")
) -> List[Dict[str, Any]]:
    """
    Загружает данные из файла и возвращает их списком операций.
    Если файл отсутствует, пустой или содержит некорректный JSON,
    возвращает пустой список.
    """
    logger.debug("Вызов dictionary_with_transaction_data с file_path=%s", file_path)
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        if isinstance(data, list):
            logger.info("Успешно загружено %d операций из %s", len(data), file_path)
            return data
        else:
            logger.error("Ожидался список операций в файле %s, получен %s", file_path, type(data).__name__)
            return []
    except FileNotFoundError as e:
        logger.error("Файл не найден: %s", file_path, exc_info=e)
        return []
    except json.JSONDecodeError as e:
        logger.error("Ошибка декодирования JSON в файле %s: %s", file_path, e, exc_info=e)
        return []


# Пример вызова функции
if __name__ == "__main__":
    file_path = os.path.join("data", "operations.json")
    transactions = dictionary_with_transaction_data(file_path)
    print(transactions)
