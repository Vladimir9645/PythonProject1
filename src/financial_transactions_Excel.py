from typing import Dict, List

import pandas as pd

# Путь к файлу Excel
file_path_2 = r"data/transactions_excel.xlsx"


def read_transactions_from_excel(file_path: str) -> List[Dict[str, str]]:
    """Для обработки выбран Excel-файл."""
    try:
        df = pd.read_excel(file_path)
        transactions: List[Dict[str, str]] = []
        for record in df.to_dict(orient="records"):
            transaction: Dict[str, str] = {}
            for key, value in record.items():
                # Гарантируем, что ключи — строки, а значения — строки
                if isinstance(key, str):
                    transaction[key] = str(value)
            transactions.append(transaction)
        return transactions
    except FileNotFoundError:
        print(f"Файл не найден: {file_path}")
        return []
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return []


# Вызов функции и вывод результатов
transactions_2 = read_transactions_from_excel(file_path_2)


