import os
from typing import Any, Dict

import requests
from dotenv import load_dotenv

load_dotenv(".env")
API_KEY = os.getenv("API_KEY")
API_URL = os.getenv("API_URL")


def convert_to_rub(
    transaction: Dict[str, Any],
    api_url: str | None = None,
    api_key: str | None = None,
) -> float:
    api_url = api_url or API_URL
    api_key = api_key or API_KEY
    if not api_url or not api_key:
        raise ValueError("API_URL и API_KEY должны быть заданы.")

    amount = float(transaction["amount"])  # предполагается, что 'amount' есть
    currency = transaction["currency"]  # предполагается, что 'currency' есть

    if currency == "RUB":
        return amount

    response = requests.get(
        api_url,
        headers={"apikey": api_key},
        params={"base": currency, "symbols": "RUB"},
    )
    response.raise_for_status()  # выбросит исключение при ошибке
    data = response.json()

    # Предполагается, что если 'success' отсутствует, всё равно можем проверить 'rates'
    rate = data.get("rates", {}).get("RUB")
    if rate is None:
        raise ValueError("Не удалось получить курс RUB из ответа API.")
    return amount * float(rate)


# Пример использования
transaction_example = {"amount": 500, "currency": "EUR"}

if __name__ == "__main__":
    print(convert_to_rub(transaction_example))
