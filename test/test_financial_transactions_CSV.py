import os
import unittest
from typing import Dict, List


def read_transactions_from_csv(file: str) -> List[Dict[str, str]]:
    import csv

    # импортирование не нужно повторно внутри функции, так как импортируете глобально в начале файла
    transactions: List[Dict[str, str]] = []
    with open(file, mode="r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            transactions.append(row)
    return transactions


class TestCSVReading(unittest.TestCase):

    def setUp(self) -> None:
        # Создаем временный файл с тестовыми данными
        self.test_filename: str = "test_transactions.csv"
        with open(self.test_filename, "w", encoding="utf-8") as f:
            f.write("date,amount,category\n")  # Заголовки
            f.write("2023-01-01,100,Food\n")  # Строка 1
            f.write("2023-01-02,200,Transport\n")  # Строка 2
            f.write("2023-01-03,300,Entertainment\n")  # Строка 3

    def tearDown(self) -> None:
        # Удаляем тестовый файл после тестов
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)

    def test_read_transactions(self) -> None:
        result: List[Dict[str, str]] = read_transactions_from_csv(
            self.test_filename
        )
        expected: List[Dict[str, str]] = [
            {"date": "2023-01-01", "amount": "100", "category": "Food"},
            {"date": "2023-01-02", "amount": "200", "category": "Transport"},
            {
                "date": "2023-01-03",
                "amount": "300",
                "category": "Entertainment",
            },
        ]
        self.assertEqual(result, expected)

    def test_empty_file(self) -> None:
        # Тест на файл без данных (только заголовки)
        empty_filename: str = "empty.csv"
        with open(empty_filename, "w", encoding="utf-8") as f:
            f.write("date,amount,category\n")
        result: List[Dict[str, str]] = read_transactions_from_csv(
            empty_filename
        )
        self.assertEqual(result, [])
        os.remove(empty_filename)
