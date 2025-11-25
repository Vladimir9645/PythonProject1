def get_exchange_rate(from_currency):
    headers = {"apikey": API_KEY}
    params = {"base": "USD", "symbols": from_currency}
    response = requests.get(API_URL, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()
    rate = data["rates"][from_currency]
    return rate


def convert_transaction_to_rub(transaction):
    amount = transaction["amount"]
    currency = transaction["currency"]
    if currency in ["USD", "EUR"]:
        rate = get_exchange_rate(currency)
        amount_in_rub = amount * rate
    else:
        amount_in_rub = amount
    return float(amount_in_rub)


transaction = {"amount": 100, "currency": "USD"}
print(convert_transaction_to_rub(transaction))
