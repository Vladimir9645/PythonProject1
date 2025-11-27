from unittest.mock import Mock, patch

import pytest

from src.external_api import convert_to_rub


def test_convert_rub_currency():
    """Тестируем для валюты RUB — сумма должна остаться без изменений."""
    transaction = {"amount": "100", "currency": "RUB"}
    result = convert_to_rub(transaction)
    assert result == 100.0


@patch("requests.get")
def test_convert_non_rub_success(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"success": True, "rates": {"RUB": 75.0}}
    mock_get.return_value = mock_response

    transaction = {"amount": "10", "currency": "USD"}
    result = convert_to_rub(transaction)  # передается по умолчанию
    assert result == 10 * 75.0
