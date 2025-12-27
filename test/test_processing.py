from datetime import datetime
from typing import Any, Dict, List, Optional

import pytest

from src.processing import filter_by_state, sort_by_date


# Фикстуры для тестирования
@pytest.fixture
def sample_data() -> List[Dict[str, Any]]:
    return [
        {"id": 1, "state": "EXECUTED", "date": "2023-01-01T10:00:00.000000"},
        {"id": 2, "state": "CANCELED", "date": "2023-01-02T10:00:00.000000"},
        {"id": 3, "state": "EXECUTED", "date": "2023-01-03T10:00:00.000000"},
        {"id": 4, "state": "PENDING", "date": "2023-01-04T10:00:00.000000"},
        {"id": 5, "state": "EXECUTED", "date": "2023-01-01T09:59:59.999999"},
    ]


@pytest.fixture
def sample_data_with_same_dates() -> List[Dict[str, Any]]:
    return [
        {"id": 10, "state": "EXECUTED", "date": "2023-01-01T10:00:00.000000"},
        {"id": 11, "state": "EXECUTED", "date": "2023-01-01T10:00:00.000000"},
    ]


@pytest.fixture
def sample_data_with_bad_date() -> List[Dict[str, Any]]:
    return [
        {
            "id": 20,
            "state": "EXECUTED",
            "date": "2023-01-01T10:00:00",
        },  # без микро секунд
        {"id": 21, "state": "EXECUTED", "date": "2023-01-01"},  # только дата
        {
            "id": 22,
            "state": "EXECUTED",
            "date": "not_a_date",
        },  # неправильный формат
    ]


# Тесты для filter_by_state
@pytest.mark.parametrize(
    "state, expected_ids",
    [
        ("EXECUTED", [1, 3, 5]),
        ("CANCELED", [2]),
        ("PENDING", [4]),
        ("UNKNOWN", []),
    ],
)
def test_filter_by_state(
    sample_data: List[Dict[str, Any]], state: str, expected_ids: List[int]
) -> None:
    """Тестирует функцию filter_by_state на корректную
     фильтрацию данных по заданному состоянию.
    sample_data — входные данные (список словарей),
    state — значение состояния для фильтрации,
    expected_ids — ожидаемые id элементов после фильтрации.
    """
    result = filter_by_state(sample_data, state)
    assert sorted(item["id"] for item in result) == sorted(expected_ids)


def test_filter_empty_list() -> None:
    """Проверяет, что filter_by_state возвращает
    пустой список при передачи пустого списка.
    """
    assert filter_by_state([], "EXECUTED") == []


# Тесты для sort_by_date


def test_sort_by_date_desc(sample_data: List[Dict[str, Any]]) -> None:
    """Проверяет сортировку по дате в порядке убывания (reverse=True)
    после фильтрации по состоянию "EXECUTED"."""
    filtered = filter_by_state(sample_data, "EXECUTED")
    sorted_list = sort_by_date(filtered, reverse=True)
    dates = [item["date"] for item in sorted_list]
    assert dates == sorted(dates, reverse=True)


def test_sort_by_date_asc(sample_data: List[Dict[str, Any]]) -> None:
    """Проверяет сортировку по дате в порядке возрастания (reverse=False)
    после фильтрации по состоянию "EXECUTED"."""
    filtered = filter_by_state(sample_data, "EXECUTED")
    sorted_list = sort_by_date(filtered, reverse=False)
    dates = [item["date"] for item in sorted_list]
    assert dates == sorted(dates, reverse=False)


def test_sort_by_date_same_dates(
    sample_data_with_same_dates: List[Dict[str, Any]],
) -> None:
    """Проверяет стабильность сортировки, когда у элементов одинаковая дата.
    Ожидается сохранение исходного порядка элементов."""
    sorted_list = sort_by_date(sample_data_with_same_dates)
    assert len(sorted_list) == 2
    # Оба элемента имеют одинаковую дату,
    # порядок должен сохраниться (стабильность сортировки)
    assert sorted_list[0]["date"] == sorted_list[1]["date"]


def test_sort_by_date_with_custom_format() -> None:
    """Проверяет сортировку с использованием пользовательского формата даты.
    Формат передается параметром date_format."""
    data = [
        {"id": 1, "date": "01-01-2023 12:00:00"},
        {"id": 2, "date": "02-01-2023 12:00:00"},
    ]
    fmt = "%d-%m-%Y %H:%M:%S"
    sorted_list = sort_by_date(data, date_format=fmt, reverse=False)
    assert sorted_list[0]["id"] == 1
    assert sorted_list[1]["id"] == 2


def test_sort_by_date_invalid_format_raises(
    sample_data_with_bad_date: List[Dict[str, Any]],
) -> None:
    """Проверяет, что при неверном формате
    даты возникает исключение ValueError."""
    # Проверяем, что при неверном формате возникает ошибка
    with pytest.raises(ValueError):
        sort_by_date(sample_data_with_bad_date)


# Тесты для комбинированного использования
def test_filter_and_sort_combined(sample_data: List[Dict[str, Any]]) -> None:
    """Проверяет корректность комбинированного
    фильтра и сортировки"""
    state = "EXECUTED"
    filtered = filter_by_state(sample_data, state)
    sorted_list = sort_by_date(filtered)
    assert all(item["state"] == state for item in sorted_list)
    # Проверить, что даты отсортированы по убыванию
    dates = [item["date"] for item in sorted_list]
    assert dates == sorted(dates, reverse=True)
