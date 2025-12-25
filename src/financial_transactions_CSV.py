import csv
from typing import Dict, List

file_path_1 = r"data/transactions.csv"


def read_transactions_from_csv(file: str) -> List[Dict[str, str]]:
    """Для обработки выбран CSV-файл."""
    transactions: List[Dict[str, str]] = []
    with open(file, mode="r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            transactions.append(row)
    return transactions

transactions_1 = read_transactions_from_csv(file_path_1)


