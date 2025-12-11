import csv
from typing import Dict, List

file = r"C:\Users\Rudoruka\PycharmProjects\PythonProject1\src\data\transactions.csv"


def read_transactions_from_csv(file: str) -> List[Dict[str, str]]:
    transactions: List[Dict[str, str]] = []
    with open(file, mode="r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            transactions.append(row)
    return transactions


print(read_transactions_from_csv(file))
