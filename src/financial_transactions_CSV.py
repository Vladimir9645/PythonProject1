import os
import csv
from typing import List, Dict

# Путь от директории текущего скрипта
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "..", "data", "transactions.csv")


def read_transactions_from_csv(file: str) -> List[Dict[str, str]]:
    """Читает транзакции из CSV‑файла и возвращает список словарей."""
    try:
        with open(file, "r", encoding="utf-8") as f:
            # Используем csv.DictReader — он автоматически берёт заголовки из первой строки
            reader = csv.DictReader(f, delimiter=";")  # Предполагаем разделитель ";"
            data = []
            for row in reader:
                # Очищаем значения от лишних пробелов
                cleaned_row = {k: v.strip() for k, v in row.items()}
                data.append(cleaned_row)
        return data
    except FileNotFoundError:
        print(f"Ошибка: файл не найден — {file}")
        return []
    except PermissionError:
        print(f"Ошибка: нет доступа к файлу — {file}")
        return []
    except UnicodeDecodeError:
        print(f"Ошибка: не удалось декодировать файл (проверьте кодировку) — {file}")
        return []
    except Exception as e:
        print(f"Неожиданная ошибка при чтении CSV: {e}")
        return []


# Вызов функции
transaction = read_transactions_from_csv(file_path)
#print(transaction)
