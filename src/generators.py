import logging
from typing import Iterator
from collections import Counter
from typing import List, Dict, Any
from src.widget import mask_account_card


def filter_by_currency(list_data, currency):
    """
    Фильтрует список транзакций по валюте (код или название).
    Args:
        list_data (list): список транзакций (словарей)
        currency (str): код или название валюты (например, "RUB", "руб.")
    Returns:
        list: отфильтрованные транзакции
    """
    # Проверка типа входных данных
    if not isinstance(list_data, list):
        logging.warning("list_data не является списком. Возвращается пустой список.")
        return []

    if not list_data:
        return []  # Пустой список на входе → пустой на выходе

    # Нормализация искомой валюты (удаление пробелов, нижний регистр)
    currency_normalized = currency.strip().lower()

    filtered = []
    for item in list_data:
        # Защита от None в списке
        if item is None:
            logging.debug("Найден None в list_data. Пропускаем.")
            continue

        # Получаем значения полей (с дефолтом "")
        code = str(item.get("currency_code", "")).strip().lower()
        name = str(item.get("currency_name", "")).strip().lower()

        # Проверка на совпадение
        if code == currency_normalized or name == currency_normalized:
            filtered.append(item)

    return filtered


transactions = [
    {
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {
            "amount": "9824.07",
            "currency": {"name": "USD", "code": "USD"},
        },
        "description": "Перевод организации",
        "from": "Счет 75106830613657916952",
        "to": "Счет 11776614605963066702",
    },
    {
        "id": 142264268,
        "state": "EXECUTED",
        "date": "2019-04-04T23:20:05.206878",
        "operationAmount": {
            "amount": "79114.93",
            "currency": {"name": "USD", "code": "USD"},
        },
        "description": "Перевод со счета на счет",
        "from": "Счет 19708645243227258542",
        "to": "Счет 75651667383060284188",
    },
    {
        "id": 873106923,
        "state": "EXECUTED",
        "date": "2019-03-23T01:09:46.296404",
        "operationAmount": {
            "amount": "43318.34",
            "currency": {"name": "руб.", "code": "RUB"},
        },
        "description": "Перевод со счета на счет",
        "from": "Счет 44812258784861134719",
        "to": "Счет 74489636417521191160",
    },
    {
        "id": 895315941,
        "state": "EXECUTED",
        "date": "2018-08-19T04:27:37.904916",
        "operationAmount": {
            "amount": "56883.54",
            "currency": {"name": "USD", "code": "USD"},
        },
        "description": "Перевод с карты на карту",
        "from": "Visa Classic 6831982476737658",
        "to": "Visa Platinum 8990922113665229",
    },
    {
        "id": 594226727,
        "state": "CANCELED",
        "date": "2018-09-12T21:27:25.241689",
        "operationAmount": {
            "amount": "67314.70",
            "currency": {"name": "руб.", "code": "RUB"},
        },
        "description": "Перевод организации",
        "from": "Visa Platinum 1246377376343588",
        "to": "Счет 14211924144426031657",
    },
]

from collections import Counter
from typing import List, Dict, Any


def count_operations_by_category(
        transactions: List[Dict[str, Any]],
        search_word: str,
        categories: List[str]
) -> Dict[str, int]:
    """
    1. Фильтрует транзакции по ключевому слову во всех текстовых полях.
    2. Подсчитывает операции по категориям (поиск в description).

    Возвращает словарь: {категория: количество}.
    """
    # Приводим поисковое слово к нижнему регистру
    search_word_lower = search_word.lower()

    # Инициализируем счётчик для категорий
    counter = {cat: 0 for cat in categories}

    # Проходим по всем транзакциям
    for trans in transactions:
        # Собираем все текстовые поля для поиска
        text_parts = []
        for field in ["description", "from", "to"]:
            value = trans.get(field, "")
            if value is not None:
                text_parts.append(str(value).lower())
        full_text = " ".join(text_parts)

        # 1. Проверяем, содержит ли транзакция поисковое слово
        if search_word_lower not in full_text:
            continue  # Пропускаем, если слово не найдено

        # 2. Проверяем, к какой категории относится транзакция
        desc = str(trans.get("description", "")).lower()
        for category in categories:
            if category.lower() in desc:
                counter[category] += 1
                break  # Зачёт только в первую подходящую категорию
    return counter


print()


def card_number_generator(start: int, end: int) -> Iterator[str]:
    """Генератор номеров банковских карт
    в формате XXXX-XXXX.
    Принимает начальное и конечное
    значения диапазона (целые числа),
    выдает номера карт в заданном
    диапазоне с ведущими нулями,
    разделенные пробелами по 4 цифры.
    """
    for number in range(start, end + 1):
        # Форматируем число с ведущими нулями до 16 цифр
        card_str = f"{number:016d}"
        # Разбиваем на группы по 4 символа и соединяем через пробел
        formatted = " ".join(card_str[i : i + 4] for i in range(0, 16, 4))
        yield formatted



# Пустая строка.
# Что-бы разделить выводы
print()
# Пример использования
# for card_number in card_number_generator(1, 5):
# print(card_number)
