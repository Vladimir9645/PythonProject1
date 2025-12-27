import csv
import os
from typing import Dict, List

# Путь от директории текущего скрипта
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path_1 = os.path.join(current_dir, "..", "data", "transactions.csv")


def read_transactions_from_csv(file: str) -> List[Dict[str, str]]:
    """Для обработки выбран CSV-файл."""
    transactions: List[Dict[str, str]] = []
    with open(file, mode="r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            transactions.append(row)
    return transactions


transaction = read_transactions_from_csv(file_path_1)
# print(transaction)
