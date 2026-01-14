from src.financial_transactions_CSV import read_transactions_from_csv
from src.financial_transactions_Excel import read_transactions_from_excel
from src.generators import filter_by_currency
from src.processing import filter_by_state
from src.utils import process_bank_search

# Sample transactions for tests
SAMPLE_TRANSACTIONS = [
    {
        "id": "tx1",
        "state": "EXECUTED",
        "date": "2019-12-08",
        "amount": 40542,
        "currency_name": "руб.",
        "currency_code": "RUB",
        "from": "Счет 1234",
        "to": "Счет 4321",
        "description": "Открытие вклада"
    },
    {
        "id": "tx2",
        "state": "EXECUTED",
        "date": "2019-11-12",
        "amount": 130,
        "currency_name": "USD",
        "currency_code": "USD",
        "from": "MasterCard 1111 27** **** 3727",
        "to": "Visa Platinum 1293 38** **** 9203",
        "description": "Перевод с карты на карту"
    },
    {
        "id": "tx3",
        "state": "PENDING",
        "date": "2018-07-18",
        "amount": 8390,
        "currency_name": "руб.",
        "currency_code": "RUB",
        "from": "Visa Platinum 7492 65** **** 7202",
        "to": "Счет 0034",
        "description": "Перевод организации"
    }
]

def test_filter_by_state_executes_expected():
    res = filter_by_state(SAMPLE_TRANSACTIONS, "EXECUTED")
    assert all(t["state"] == "EXECUTED" for t in res)
    assert len(res) == 2



def test_filter_by_currency_rub():
    rubs = list(filter_by_currency(SAMPLE_TRANSACTIONS, "RUB"))
    assert len(rubs) == 2
    assert all(t["currency_code"] in ("RUB",) for t in rubs)  # still RUB

def test_process_bank_search_matches_description():
    word = "вклада"
    res = process_bank_search(SAMPLE_TRANSACTIONS, word)
    assert len(res) == 1
    assert res[0]["description"] == "Открытие вклада"

