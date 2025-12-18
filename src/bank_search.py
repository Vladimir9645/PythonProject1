import re
from collections import Counter


def process_bank_search(data: list[dict], search: str) -> list[dict]:
    """ Ищет в списке банковских операций те операции,
       у которых в описании есть строка """
    pattern = re.compile(search, re.IGNORECASE)  # Регулярное выражение без учета регистра
    result = []

    for transaction in data:
        description = transaction.get('description', '')
        if pattern.search(description):
            result.append(transaction)

    return result


def count_transactions_by_category(transactions, categories):
    """ Подсчитывает количество транзакций,
    соответствующих заданным категориям."""
    # Создаем список категорий для транзакций, где description содержит название категории
    matched_categories = [
        category for transaction in transactions
        for category in categories
        if category in transaction.get('description', '')
    ]

    # Используем Counter для подсчета количества каждой категории
    counter = Counter(matched_categories)

    # Преобразуем Counter в словарь
    result = dict(counter)

    return result

