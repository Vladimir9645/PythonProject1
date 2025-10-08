"""Обрабатывает информацию как о картах, так и о счетах."""

from src.masks import get_mask_account, get_mask_card_number
from datetime import datetime


def mask_account_card(input_str: str) -> str:

    """ Принимает строку формата:
    - "Visa Platinum 7000792289606361"
    - "Maestro 7000792289606361"
    - "Счет 73654108430135874305"
    Возвращает строку с замаскированным номером. """

    card_types = ['Maestro', 'MasterCard',
                  'Visa Classic', 'Visa Platinum',
                  'Visa Gold'
                  ]
    account_types = ['Счет']

    input_str = input_str.strip()
    parts = input_str.split()

    # Определяем тип карты/счёта и номер (номер - всегда последний элемент)
    name = " ".join(parts[:-1])
    number = parts[-1]

    if name in card_types:
        masked_number = get_mask_card_number(number)
        return f"{name} {masked_number}"
    elif name in account_types:
        masked_number = get_mask_account(number)
        return f"{name} {masked_number}"
    else:
        return "Неизвестный тип карты или счёта"


# Пример вызова
print(mask_account_card("Visa Platinum 7000792289606361"))
print(mask_account_card("Maestro 7000792289606361"))
print(mask_account_card("Счет 73654108430135874305"))


""" Принимает строку с датой в формате "2024-03-11T02:26:18.671407"
и возвращает строку с датой в формате "ДД.ММ.ГГГГ" """


def get_date(date_str: str) -> str:
    """Принимает строку с датой в формает и возвращает строку с датой."""
    # Переносим входную строку в объект datetime
    dt = datetime.fromisoformat(date_str)
    # Форматируем дату в нужный формат: День.Месяц.Год
    return dt.strftime("%d.%m.%Y")


# Пример использования:
# Выведет: 11.03.2024
print(get_date("2024-03-11T02:26:18.671407"))
