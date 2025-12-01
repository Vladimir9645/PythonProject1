import os
from typing import Any, Dict

import requests
from dotenv import load_dotenv

load_dotenv(".env")
API_KEY = os.getenv("API_KEY")
API_URL = os.getenv("API_URL")

if API_KEY is None:
    raise ValueError("API_KEY не установлен в .env")
if API_URL is None:
    raise ValueError("API_URL не установлен в .env")


def convert_to_rub(
    transaction: Dict[str, Any],
    api_url: str | None = None,
    api_key: str | None = None,
) -> float:
    if api_url is None:
        api_url = API_URL
    if api_key is None:
        api_key = API_KEY

    if api_url is None or api_key is None:
        raise ValueError("API_URL и API_KEY должны быть заданы")

    amount = transaction.get("amount")
    currency = transaction.get("currency")

    if amount is None or currency is None:
        raise ValueError("Отсутствуют amount или currency")
    amount = float(amount)

    if currency == "RUB":
        return amount

    response = requests.get(
        api_url,
        headers={"apikey": api_key},
        params={"base": currency, "symbols": "RUB"},
    )

    if response.status_code != 200:
        raise ValueError(
            f"Ошибка запроса к API: статус {response.status_code}"
        )

    data = response.json()
    if not data.get("success", False):
        raise ValueError(
            "API вернул unsuccessful статус или ключ 'success' отсутствует"
        )
    if "rates" not in data or "RUB" not in data["rates"]:
        raise ValueError("Отсутствуют необходимые курсы в ответе API")

    rate = data["rates"]["RUB"]
    if rate is None:
        raise ValueError("Курс RUB отсутствует в данных")

    return amount * float(rate)


# Пример использования
transaction_example = {"amount": 500, "currency": "EUR"}

if __name__ == "__main__":
    print(convert_to_rub(transaction_example))
