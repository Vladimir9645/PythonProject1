import os
from unittest.mock import Mock, patch

import pytest

os.environ["API_KEY"] = "test_key"
os.environ["API_URL"] = "https://mockapi.test"

from src.external_api import convert_to_rub


def test_convert_rub_currency() -> None:
    """Тестируем для валюты RUB — сумма должна остаться без изменений."""
    transaction = {"amount": "100", "currency": "RUB"}
    result = convert_to_rub(transaction)
    assert result == 100.0


def test_missing_rub_in_rates() -> None:
    """Обработка отсутствия ключа 'RUB' в 'rates'."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"success": True, "rates": {"USD": 1.2}}
    with patch("requests.get", return_value=mock_response):
        with pytest.raises(ValueError):
            convert_to_rub({"amount": 10, "currency": "USD"})
