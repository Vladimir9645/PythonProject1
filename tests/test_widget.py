import pytest
from datetime import datetime
from src.widget import mask_account_card, get_date

# Тесты для mask_account_card

@pytest.mark.parametrize("input_str,expected", [
    ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
    ("Maestro 7000792289606361", "Maestro 7000 79** **** 6361"),
    ("MasterCard 1234567890123456", "MasterCard 1234 56** **** 3456"),
    ("Visa Classic 1234567812345678", "Visa Classic 1234 56** **** 5678"),
    ("Visa Gold 1234567890123456", "Visa Gold 1234 56** **** 3456"),
    ("Счет 73654108430135874305", "Счет **4305"),
])
def test_mask_account_card_valid(input_str, expected):
    assert mask_account_card(input_str) == expected

@pytest.mark.parametrize("input_str", [
    "", # Пустая строка
    "Unknown 1234567890123456",  # неизвестный тип
    "Visa 123456",  # неполный номер
    "Счет ",  # отсутствует номер
    "Maestro",  # отсутствует номер
])
def test_mask_account_card_invalid(input_str):
    assert mask_account_card(input_str) == "Неизвестный тип карты или счёта"

# Тесты для get_date

@pytest.mark.parametrize("input_str,expected", [
    ("2024-03-11T02:26:18.671407", "11.03.2024"),
    ("2020-01-01T00:00:00", "01.01.2020"),
    ("1999-12-31T23:59:59", "31.12.1999"),
])
def test_get_date_valid(input_str, expected):
    assert get_date(input_str) == expected

@pytest.mark.parametrize("input_str", [
    "",  # пустая строка
    "2024-13-01T00:00:00",  # некорректный месяц
    "2024-00-10T00:00:00",  # некорректный месяц 0
    "2024-02-30T00:00:00",  # несуществующая дата
    "some random string",  # совсем не дата
])
def test_get_date_invalid(input_str):
    with pytest.raises(Exception):
        get_date(input_str)







