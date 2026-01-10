from datetime import datetime
from typing import Any, Dict, List
from collections import Counter


def filter_by_state(
    list_data: list[dict], state: str = "EXECUTED"
) -> List[dict]:
    """Фильтрует транзакции по полю 'state' (с отладкой)."""
    return [
        dict_data_state
        for dict_data_state in list_data
        if dict_data_state.get("state", "") == state
    ]


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
    date_formats: List[str] = None,
    reverse: bool = True,
) -> List[Dict[str, Any]]:
    """
    Сортирует список словарей по дате, пробуя несколько форматов.
    Записи с невалидной датой помещаются в конец (при reverse=False) или начало (при reverse=True).
    """
    if date_formats is None:
        date_formats = [
            "%Y-%m-%dT%H:%M:%S.%fZ",
            "%Y-%m-%dT%H:%M:%SZ",
            "%Y-%m-%d %H:%M:%S",
            "%d.%m.%Y %H:%M:%S",
            "%Y-%m-%d",
        ]

    def parse_date(date_str: str) -> datetime:
        """Возвращает datetime или очень большое/маленькое значение для сортировки."""
        for fmt in date_formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        # Если дата не распознана:
        if reverse:  # По убыванию → невалидные даты в начало
            return datetime.min  # Минимальное возможное время
        else:       # По возрастанию → невалидные даты в конец
            return datetime.max  # Максимальное возможное время

    return sorted(
        dictionary_2,
        key=lambda d: parse_date(d.get(date_key, "")),
        reverse=reverse
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
sorted_filtered = sort_by_date(filtered)



# Фильтруем словарь по состоянию 'CANCELED'
filtered = filter_by_state(dictionary, "CANCELED")
sorted_filtered = sort_by_date(filtered)


filtered = filter_by_state(dictionary, "PENDING")
sorted_filtered = sort_by_date(filtered)


# Использование функции сортировки
sorted_events = sort_by_date(dictionary, "date")
# print(sorted_events)

