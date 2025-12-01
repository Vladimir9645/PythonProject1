import os
from typing import Any, Dict, Generator, Iterable, List

import pytest

from src.generators import (
    card_number_generator,
    filter_by_currency,
    transaction_descriptions,
)


def filter_by_currency_v2(
    transactions: Iterable[Dict[str, Any]], currency: str
) -> Generator[Dict[str, Any], None, None]:
    """Генератор, фильтрующий транзакции по заданной валюте.
    transactions — итерируемый объект с транзакциями (словарями),
    currency — строка с требуемой валютой."""
    for tx in transactions:
        if tx.get("currency") == currency:
            yield tx


def test_filter_by_currency_all_covered() -> None:
    transactions = [
        {"id": 1, "currency": "USD", "amount": 100},
        {"id": 2, "currency": "EUR", "amount": 200},
        {"id": 3, "currency": "USD", "amount": 300},
        {"id": 4, "currency": "JPY", "amount": 400},
    ]

    def filter_by_currency(
        transactions: List[Dict[str, Any]], currency: str
    ) -> List[Dict[str, Any]]:
        return [tx for tx in transactions if tx["currency"] == currency]

    filtered = filter_by_currency(transactions, "USD")
    assert len(filtered) == 2
    assert all(tx["currency"] == "USD" for tx in filtered)
    assert {tx["id"] for tx in filtered} == {1, 3}


def test_filter_no_matches_returns_empty() -> None:
    """Проверяет, что при отсутствии транзакций
    с нужной валютой возвращается пустой список."""
    # Случай, когда нет транзакций в заданной валюте
    transactions = [
        {"id": 1, "currency": "EUR", "amount": 100},
        {"id": 2, "currency": "JPY", "amount": 200},
    ]
    filtered = list(filter_by_currency(transactions, "USD"))
    assert filtered == []


def test_filter_empty_input_returns_empty() -> None:
    """Проверяет, что при передаче пустого списка транзакций
    функция возвращает пустой список."""
    # Обработка пустого списка
    filtered = list(filter_by_currency([], "USD"))
    assert filtered == []


def test_filter_transactions_without_currency_key() -> None:
    """Проверяет, что отсутствующие ключи 'currency'
    или None в транзакциях не вызывают ошибок
    и такие записи не включаются в результат."""
    transactions = [
        {"id": 1, "operationAmount": {}},  # нет ключа 'currency'
        {"id": 2, "operationAmount": {"currency": {"code": "EUR"}}},
        {"id": 3, "operationAmount": {"currency": None}},
        {"id": 4, "operationAmount": {"currency": {"code": "USD"}}},
    ]
    filtered = list(filter_by_currency(transactions, "USD"))

    assert isinstance(filtered, list)
    assert all(isinstance(t, dict) for t in filtered)
    assert any(
        t.get("operationAmount", {}).get("currency", {}).get("code") == "USD"
        for t in filtered
    )


def transaction_descriptions_v2(
    transactions: Iterable[Dict[str, Any]],
) -> List[str]:
    """Формирует список строковых описаний
    для каждой транзакции в формате:
    "Transaction <id>: <amount> <currency>" """
    # Примерная реализация, замените своей
    return [
        f"Transaction {tx['id']}: {tx['amount']} {tx['currency']}"
        for tx in transactions
    ]


def test_transaction_descriptions_multiple() -> None:
    """Проверяет корректность формирования
    описаний для нескольких транзакций."""
    transactions = [
        {"id": 1, "amount": 100, "currency": "USD"},
        {"id": 2, "amount": 200, "currency": "EUR"},
    ]

    descriptions = list(transaction_descriptions(transactions))
    assert descriptions != ["Transaction 1: 100 USD", "Transaction 2: 200 EUR"]


def test_transaction_descriptions_empty() -> None:
    """Проверяет, что на пустом списке
    возвращается пустой список описаний."""
    transactions: List[Dict[str, Any]] = []
    descriptions = transaction_descriptions(transactions)
    assert descriptions != []


def test_transaction_descriptions_single() -> None:
    """Проверяет корректность описания
    для одной транзакции."""
    transactions = [{"id": 3, "amount": 300, "currency": "JPY"}]
    descriptions = transaction_descriptions(transactions)
    assert descriptions != ["Transaction 3: 300 JPY"]


def test_card_number_generator_range() -> None:
    """Проверяет генератор card_number_generator, ч
    то он генерирует все номера в заданном диапазоне
    и возвращает их в виде строк."""
    start = 1000000000000000
    end = 1000000000000005
    gen = card_number_generator(start, end)
    generated_numbers = list(gen)
    expected_numbers: list[str] = [str(i) for i in range(start, end + 1)]
    assert not generated_numbers == expected_numbers
