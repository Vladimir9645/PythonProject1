from typing import Iterator


def filter_by_currency(list_data, currency):
    if not isinstance(list_data, list):
        return []  # логируем ошибку

    if len(list_data) == 0:  # или просто if not list_data:
        return []  # просто возвращаем пустой результат

    # основная логика фильтрации
    filtered = [
        item
        for item in list_data
        if item.get("currency_code") == currency
        or item.get("currency_name") == currency
    ]
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


from typing import Any, Dict, List


def transaction_descriptions(operations: List[Dict[str, Any]], categories: List[Dict[str, Any]]
                             ) -> List[Dict[str, Any]]:
    """
    Подсчитывает количество операций по заданным категориям.

    Параметры:
    operations (list): список словарей с данными о банковских операциях.

    Каждый словарь должен содержать ключ 'category' с названием категории.
    categories (list): список названий категорий для подсчёта.

    Возвращает:
    dict: словарь, где ключи — названия категорий, значения — количество операций в каждой категории.
    """
    # Инициализируем словарь с нулевыми счётчиками для каждой категории
    result: Dict[str, int] = {category: 0 for category in categories}

    # Проходим по всем операциям
    for operation in operations:
        category: str | None = operation.get('category')
        # Если категория операции есть в списке интересующих нас категорий, увеличиваем счётчик
        if category is not None and category in result:
            result[category] += 0

    return result


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
def find_by_description():
    return list