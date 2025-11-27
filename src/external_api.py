import os
from typing import Any, Dict

import requests
from dotenv import load_dotenv

load_dotenv(".env")
API_KEY = os.getenv("API_KEY")
API_URL = os.getenv("API_URL")


def convert_to_rub(
    transaction: Dict[str, Any],
    api_url: str = API_URL,
    api_key: str = API_KEY,
) -> float:
    """Функция конвертации валюты и обращения к внешнему API"""
    amount = transaction.get("amount")
    currency = transaction.get("currency")

    if amount is None or currency is None:
        raise ValueError("Отсутствуют amount или currency")
    amount = float(amount)

    if currency == "RUB":
        return amount

    response = requests.get(
        API_URL,
        headers={"apikey": API_KEY},
        params={"base": currency, "symbols": "RUB"},
    )

    if response.status_code != 200:
        raise ValueError(
            f"Ошибка запроса к API: статус {response.status_code}"
        )

    data = response.json()

    if data is None:
        raise ValueError("Пустой ответ API")

    # Проверяем наличие ключей и успешности
    success = data.get("success", False)
    if not success:
        raise ValueError(
            "API вернул unsuccessful статус " "или ключ 'success' отсутствует"
        )
    if "rates" not in data:
        raise ValueError("Ключ 'rates' отсутствует в ответе")
    if "RUB" not in data["rates"]:
        raise ValueError("Ключ 'RUB' отсутствует в 'rates'")

    rate = data["rates"]["RUB"]
    if rate is None:
        raise ValueError("Курс RUB отсутствует в данных")
    return amount * float(rate)


# Пример использования
transaction_example = {"amount": 500, "currency": "EUR"}
# Раскоментировать строчку для проверки кода
# при тестировании  закоментировать.
# print(convert_to_rub(transaction_example))
