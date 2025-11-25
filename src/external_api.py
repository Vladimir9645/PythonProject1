import json
import os

import requests
from dotenv import load_dotenv

load_dotenv(".env")
API_KEY = os.getenv("API_KEY")
API_URL = os.getenv("API_URL")


def convert_to_rub(transaction):
    """Функция конвертации валюты
    и обращения к внешнему API"""
    amount, currency = transaction.get("amount"), transaction.get("currency")
    if not amount or not currency:
        raise ValueError("Отсутствуют amount или currency")
    if currency == "RUB":
        return float(amount)

    response = requests.get(
        API_URL,
        headers={"apikey": API_KEY},
        params={"base": currency, "symbols": "RUB"},
    )

    if response.status_code != 200:
        raise ValueError(
            f"Ошибка запроса к API: " f"статус {response.status_code}"
        )

    data = response.json()

    # Добавим проверку ключей и успешности запроса
    if (
        not data.get("success")
        or "rates" not in data
        or "RUB" not in data["rates"]
    ):
        raise ValueError("Ошибка получения курса RUB")

    rate = data["rates"]["RUB"]
    return float(amount) * rate


# Пример использования
transaction_example = {"amount": 500, "currency": "EUR"}
# Раскоментировать строчку для проверки кода
# при тестировании  закоментировать.
print(convert_to_rub(transaction_example))
