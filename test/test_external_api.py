import os
import unittest
from typing import Any, Dict
from unittest.mock import Mock, patch

from dotenv import load_dotenv

from src.external_api import convert_to_rub

load_dotenv(".env")

import src.external_api as ext_api

# Устанавливаем переменные внутри модуля
ext_api.API_URL = os.getenv("API_URL", "https://example.com/api")
ext_api.API_KEY = os.getenv("API_KEY", "test_api_key")


class TestConvertToRub(unittest.TestCase):
    """Тесты функции convert_to_rub."""

    @patch("src.external_api.requests.get")
    def test_rub_currency_returns_same_amount(self, mock_get: Mock) -> None:
        transaction: Dict[str, Any] = {"amount": "150", "currency": "RUB"}

        result: float = convert_to_rub(transaction)

        self.assertEqual(result, 150.0)
        mock_get.assert_not_called()

    @patch("src.external_api.requests.get")
    def test_non_rub_currency_successful_conversion(
        self, mock_get: Mock
    ) -> None:
        transaction: Dict[str, Any] = {"amount": "200", "currency": "USD"}

        mock_response: Mock = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "rates": {"RUB": 75.5},
        }
        mock_get.return_value = mock_response

        expected: float = 200 * 75.5

        result: float = convert_to_rub(transaction)

        self.assertAlmostEqual(result, expected)

        mock_get.assert_called_once_with(
            ext_api.API_URL,
            headers={"apikey": ext_api.API_KEY},
            params={"base": "USD", "symbols": "RUB"},
        )


if __name__ == "__main__":
    unittest.main()
