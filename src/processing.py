from datetime import datetime
from typing import Any, Dict, List


def filter_by_state(
    list_data: list[dict], state: str = "EXECUTED"
) -> List[dict]:
    """Фильтрует транзакции по полю 'state' (с отладкой)."""
    return [
        dict_data_state
        for dict_data_state in list_data
        if dict_data_state.get("state", "") == state
    ]


def process_bank_operations(
    data: List[Dict[str, Any]], categories: List[str]
) -> Dict[str, int]:
    """
    Подсчитывает количество операций в каждой из указанных категорий.
    Категория определяется по наличию подстроки в поле 'description'.


    Args:
        data: список словарей с данными о банковских операциях
        categories: список строк-категорий для поиска


    Returns:
        Словарь: ключ — название категории, значение — количество операций
    """
    if not data or not categories:
        return {category: 0 for category in categories}

    # Инициализируем словарь результатов
    result = {category: 0 for category in categories}

    for operation in data:
        description = operation.get("description", "").lower()
        for category in categories:
            if category.lower() in description:
                result[category] += 1

    return result


# operations = [
#   {"id": 1, "description": "Перевод другу 500 руб."},
#  {"id": 2, "description": "Оплата интернета МТС"},
# {"id": 3, "description": "Покупка продуктов в Пятёрочке"},
# {"id": 4, "description": "Перевод сестре 1000 руб."}
# ]

# categories = ["перевод", "оплата", "покупка"]
# counts = process_bank_operations(operations, categories)
# Вернёт: {"перевод": 2, "оплата": 1, "покупка": 1}


def sort_by_date(
    dictionary_2: List[Dict[str, Any]],
    date_key: str = "date",
    date_format: str = "%Y-%m-%dT%H:%M:%S.%f",
    reverse: bool = True,
) -> List[Dict[str, Any]]:
    """Сортирует список словарей по дате,
    учитывая формат даты с временем и миллисекундами"""
    return sorted(
        dictionary_2,
        key=lambda d: datetime.strptime(d[date_key], date_format),
        reverse=reverse,
    )


# код сортирует список словарей по дате,
# указанной в каждом словаре,
# в том порядке, который задаётся переменной reverse


# Исходный список словарей
dictionary = [
    {
        "id": 41428829,
        "state": "EXECUTED",
        "date": "2019-07-03T18:35:29.512364",
    },
    {
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
    },
    {
        "id": 594226727,
        "state": "CANCELED",
        "date": "2018-09-12T21:27:25.241689",
    },
    {
        "id": 615064591,
        "state": "CANCELED",
        "date": "2018-10-14T08:21:33.419441",
    },
]

# Фильтруем словарь по состоянию 'EXECUTED'
filtered = filter_by_state(dictionary, "EXECUTED")
# Сортируем отфильтрованные данные по дате
sorted_filtered = sort_by_date(filtered)
# Выводим отсортированные данные для состояния 'EXECUTED'
# print(sorted_filtered)


# Фильтруем словарь по состоянию 'CANCELED'
filtered = filter_by_state(dictionary, "CANCELED")
# Сортируем отфильтрованные данные по дате
sorted_filtered = sort_by_date(filtered)
# Выводим отсортированные данные для состояния 'CANCELED'
# print(sorted_filtered)
# пустая строка
# print()

# Использование функции сортировки
sorted_events = sort_by_date(dictionary, "date")
# print(sorted_events)
