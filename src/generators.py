import functools
import traceback
from typing import Any, Callable, Dict, Iterator, List, Optional


def filter_by_currency(
    transactions: List[Dict[str, Any]], currency_code: str
) -> List[Dict[str, Any]]:
    filtered: List[Dict[str, Any]] = []
    for transaction in transactions:
        op_amount = transaction.get("operationAmount", {})
        currency = op_amount.get("currency")
        if currency and isinstance(currency, dict):
            code = currency.get("code")
            if code == currency_code:
                filtered.append(transaction)
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

usd_transactions = filter_by_currency(transactions, "USD")
usd_iter = iter(usd_transactions)
print(next(usd_iter))


def transaction_descriptions(
    transactions: List[Dict[str, Any]],
) -> Iterator[str]:
    """
    Функция выводит описание каждой транзакции из списка.
    """
    for transaction in transactions:
        try:
            yield transaction["description"]
        except KeyError:
            continue


descriptions = transaction_descriptions(transactions)
print()  # Пустая строка.
# чтобы разделить выводы

# Вывод первых 5 описаний транзакций в нужном формате
for _ in range(5):
    print(next(descriptions))  # Последующие с отступом


def card_number_generator(start: int, end: int) -> Iterator[str]:
    """Генератор номеров банковских карт
    в формате XXXX XXXX XXXX XXXX.
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
        formatted = " ".join(card_str[i:i + 4] for i in range(0, 16, 4))
        yield formatted


# Пустая строка.
# что-бы разделить выводы
print()
# Пример использования
for card_number in card_number_generator(1, 5):
    print(card_number)
