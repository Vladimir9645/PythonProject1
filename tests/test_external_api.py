import pytest
from unittest.mock import patch, Mock
from src.external_api import convert_to_rub



API_URL = "https://api.example.com"  # замените на актуальный URL
API_KEY = "test_api_key"

def test_convert_rub_currency():
    """Тестируем для валюты RUB — сумма должна остаться без изменений."""
    transaction = {"amount": "100", "currency": "RUB"}
    result = convert_to_rub(transaction)
    assert result == 100.0

@patch('requests.get')
def test_convert_non_rub_success(mock_get):
    """Тест успешной конвертации для валюты EUR/USD."""
    # Мокаем ответ API
    mock_response = Mock()
    mock_response.status_code = 200
    # Представим, что курс 1 EUR или USD к RUB равен 75.0
    mock_response.json.return_value = {
        "success": True,
        "rates": {"RUB": 75.0}
    }
    mock_get.return_value = mock_response

    transaction = {"amount": "10", "currency": "USD"}
    result = convert_to_rub(transaction)
    assert result == 10 * 75.0








