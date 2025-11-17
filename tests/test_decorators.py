import traceback
from pathlib import Path

import pytest

from src.decorators import log


def test_log_decorator_console_success(capsys):
    @log()
    def add(x, y):
        return x + y

    # вызываем декорированную функцию
    result = add(2, 3)
    assert result == 5

    # перехватываем вывод в консоль
    captured = capsys.readouterr().out

    # проверяем, что логи в консоли содержат ожидаемые строчки
    assert "Начало выполнения функции add" in captured
    assert "Результат: 5" in captured
    assert "Функция add выполнена успешно" in captured


def test_log_decorator_console_exception(capsys):
    @log()
    def fail():
        raise ValueError("Test error")

    # ожидаем, что при вызове будет прокинуто ValueError
    with pytest.raises(ValueError):
        fail()

    captured = capsys.readouterr().out

    # проверяем, что начало выполнения залогировано
    # и потом появилась информация об ошибке
    assert "Начало выполнения функции fail" in captured
    assert "Ошибка в функции fail: Test error" in captured
    # часть трейсбэка
    assert "ValueError: Test error" in captured


def test_log_decorator_file_success(tmp_path):
    log_file = tmp_path / "success.log"

    @log(str(log_file))
    def multiply(a, b):
        return a * b

    result = multiply(4, 5)
    assert result == 20

    # читаем содержимое файла
    content = log_file.read_text(encoding="utf-8")

    assert "Начало выполнения функции multiply" in content
    assert "Результат: 20" in content
    assert "Функция multiply выполнена успешно" in content


def test_log_decorator_file_exception(tmp_path):
    log_file = tmp_path / "error.log"

    @log(str(log_file))
    def fail():
        raise RuntimeError("Failure")

    with pytest.raises(RuntimeError):
        fail()

    content = log_file.read_text(encoding="utf-8")

    assert "Начало выполнения функции fail" in content
    assert "Ошибка в функции fail: Failure" in content
    # проверяем, что трейсбэк тоже попал в лог
    assert "RuntimeError: Failure" in content
