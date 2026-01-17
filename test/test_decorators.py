from pathlib import Path

import pytest

from src.decorators import log


def test_log_decorator_console_success(
    capsys: pytest.CaptureFixture[str],
) -> None:
    @log()
    def add(x: float, y: float) -> float:
        return x + y

    result: float = add(2, 3)
    assert result == 5

    # перехватываем вывод
    captured: str = capsys.readouterr().out
    assert "Начало выполнения функции add" in captured
    assert "Результат: 5" in captured
    assert "Функция add выполнена успешно" in captured


def test_log_decorator_console_exception(
    capsys: pytest.CaptureFixture[str],
) -> None:
    @log()
    def fail() -> None:
        raise ValueError("Test error")

    with pytest.raises(ValueError):
        fail()

    captured: str = capsys.readouterr().out
    assert "Начало выполнения функции fail" in captured
    assert "Ошибка в функции fail: Test error" in captured
    assert "ValueError: Test error" in captured


def test_log_decorator_file_success(tmp_path: "Path") -> None:
    log_file = tmp_path / "success.log"

    @log(str(log_file))
    def multiply(a: float, b: float) -> float:
        return a * b

    result: float = multiply(4, 5)
    assert result == 20

    # читаем содержимое файла
    content: str = log_file.read_text(encoding="utf-8")
    assert "Начало выполнения функции multiply" in content
    assert "Результат: 20" in content
    assert "Функция multiply выполнена успешно" in content


def test_log_decorator_file_exception(tmp_path: "Path") -> None:
    log_file = tmp_path / "error.log"

    @log(str(log_file))
    def fail() -> None:
        raise RuntimeError("Failure")

    with pytest.raises(RuntimeError):
        fail()

    content: str = log_file.read_text(encoding="utf-8")
    assert "Начало выполнения функции fail" in content
    assert "Ошибка в функции fail: Failure" in content
    assert "RuntimeError: Failure" in content
