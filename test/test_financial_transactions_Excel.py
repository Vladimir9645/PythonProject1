import os
import tempfile
import unittest
from typing import Dict, List

import pandas as pd


def read_transactions_from_excel(file_path: str) -> List[Dict[str, str]]:
    try:
        df = pd.read_excel(file_path)
        transactions: List[Dict[str, str]] = []
        for record in df.to_dict(orient="records"):
            transaction: Dict[str, str] = {}
            for key, value in record.items():
                # Приведение ключа к str, если нужно
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


class TestReadTransactionsFromExcel(unittest.TestCase):
    def setUp(self) -> None:
        # Создаем временный файл Excel с тестовыми данными
        self.temp_dir: tempfile.TemporaryDirectory = (
            tempfile.TemporaryDirectory()
        )
        self.file_path: str = os.path.join(
            self.temp_dir.name, "test_transactions.xlsx"
        )
        df: pd.DataFrame = pd.DataFrame(
            {
                "date": ["2023-01-01", "2023-01-02"],
                "amount": [100, 200],
                "category": ["Food", "Transport"],
            }
        )
        df.to_excel(self.file_path, index=False)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_read_transactions(self) -> None:
        result: List[Dict[str, str]] = read_transactions_from_excel(
            self.file_path
        )
        expected: List[Dict[str, str]] = [
            {"date": "2023-01-01", "amount": "100", "category": "Food"},
            {"date": "2023-01-02", "amount": "200", "category": "Transport"},
        ]
        self.assertEqual(result, expected)

    def test_file_not_found(self) -> None:
        # Пробуем читать несуществующий файл
        result: List[Dict[str, str]] = read_transactions_from_excel(
            "несуществующий_файл.xlsx"
        )
        self.assertEqual(result, [])

    def test_empty_sheet(self) -> None:
        # Создаём пустой Excel (только заголовки)
        empty_path: str = os.path.join(self.temp_dir.name, "empty.xlsx")
        pd.DataFrame(columns=["date", "amount", "category"]).to_excel(
            empty_path, index=False
        )
        result: List[Dict[str, str]] = read_transactions_from_excel(empty_path)
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
