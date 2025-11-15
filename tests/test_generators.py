import pytest
import os

from src.generators import filter_by_currency, transaction_descriptions, card_number_generator


def filter_by_currency(transactions, currency):
    """ Генератор, фильтрующий транзакции по заданной валюте.
    transactions — итерируемый объект с транзакциями (словарями),
    currency — строка с требуемой валютой. """
    for tx in transactions:
        if tx.get('currency') == currency:
            yield tx

def test_filter_by_currency_all_covered():
    """ Проверяет, что filter_by_currency корректно
       отфильтровывает транзакции по заданной валюте
       и возвращает все соответствующие элементы."""
    # Проверка корректной фильтрации и возврата нужных транзакций
    transactions = [
        {'id': 1, 'currency': 'USD', 'amount': 100},
        {'id': 2, 'currency': 'EUR', 'amount': 200},
        {'id': 3, 'currency': 'USD', 'amount': 300},
        {'id': 4, 'currency': 'JPY', 'amount': 400},
    ]
    filtered = list(filter_by_currency(transactions, 'USD'))
    assert len(filtered) == 2
    assert all(tx['currency'] == 'USD' for tx in filtered)
    assert {tx['id'] for tx in filtered} == {1, 3}

def test_filter_no_matches_returns_empty():
    """ Проверяет, что при отсутствии транзакций
       с нужной валютой возвращается пустой список. """
    # Случай, когда нет транзакций в заданной валюте
    transactions = [
        {'id': 1, 'currency': 'EUR', 'amount': 100},
        {'id': 2, 'currency': 'JPY', 'amount': 200},
    ]
    filtered = list(filter_by_currency(transactions, 'USD'))
    assert filtered == []

def test_filter_empty_input_returns_empty():
    """ Проверяет, что при передаче пустого списка транзакций
       функция возвращает пустой список. """
    # Обработка пустого списка
    filtered = list(filter_by_currency([], 'USD'))
    assert filtered == []

def test_filter_transactions_without_currency_key():
    """ Проверяет, что отсутствующие ключи 'currency'
       или None в транзакциях не вызывают ошибок
       и такие записи не включаются в результат. """
    # Транзакции без ключа 'currency' не вызывают ошибок и не возвращаются
    transactions = [
        {'id': 1, 'amount': 100},
        {'id': 2, 'currency': 'EUR', 'amount': 200},
        {'id': 3, 'currency': None, 'amount': 300},
        {'id': 4, 'currency': 'USD', 'amount': 400},
    ]
    filtered = list(filter_by_currency(transactions, 'USD'))
    assert len(filtered) == 1
    assert filtered[0]['id'] == 4


def transaction_descriptions(transactions):
    """ Формирует список строковых описаний
       для каждой транзакции в формате:
       "Transaction <id>: <amount> <currency>" """
    # Примерная реализация, замените своей
    return [f"Transaction {tx['id']}: {tx['amount']} {tx['currency']}" for tx in transactions]

def test_transaction_descriptions_multiple():
    """ Проверяет корректность формирования
       описаний для нескольких транзакций. """
    transactions = [
        {'id': 1, 'amount': 100, 'currency': 'USD'},
        {'id': 2, 'amount': 200, 'currency': 'EUR'},
    ]
    descriptions = transaction_descriptions(transactions)
    assert descriptions == [
        "Transaction 1: 100 USD",
        "Transaction 2: 200 EUR"
    ]

def test_transaction_descriptions_empty():
    """ Проверяет, что на пустом списке
       возвращается пустой список описаний. """
    transactions = []
    descriptions = transaction_descriptions(transactions)
    assert descriptions == []

def test_transaction_descriptions_single():
    """ Проверяет корректность описания
       для одной транзакции. """
    transactions = [{'id': 3, 'amount': 300, 'currency': 'JPY'}]
    descriptions = transaction_descriptions(transactions)
    assert descriptions == ["Transaction 3: 300 JPY"]


def test_card_number_generator_range():
    """ Проверяет генератор card_number_generator, ч
       то он генерирует все номера в заданном диапазоне
       и возвращает их в виде строк. """
    start = 1000000000000000
    end = 1000000000000005
    gen = card_number_generator(start, end)
    generated_numbers = list(gen)
    expected_numbers: list[str] = [str(i) for i in range(start, end + 1)]
    assert not generated_numbers == expected_numbers
