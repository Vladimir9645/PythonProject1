import pytest
import os

from src.decorators import log


# Функция для тестов
@log(filename="mylog.txt")
def my_function(x, y):
    return x + y


@log(filename="mylog.txt")
def error_function():
    raise ValueError("Что-то пошло не так")


# Тест успешного выполнения
def test_my_function_success(capsys):
    if os.path.exists("mylog.txt"):
        os.remove("mylog.txt")

    result = my_function(1, 2)
    captured = capsys.readouterr()

    assert result == 3
    assert "Успешно выполнена моя функция" in captured.out

    with open("mylog.txt") as f:
        content = f.read()
    assert "Функция my_function вызвана успешно с результатом: 3" in content


# Тест обработки исключения
def test_error_function_exception(capsys):
    if os.path.exists("mylog.txt"):
        os.remove("mylog.txt")

    with pytest.raises(ValueError, match="Что-то пошло не так"):
        error_function()
    captured = capsys.readouterr()

    assert "Исключение в error_function: что-то пошло не так" in captured.out

    with open("mylog.txt") as f:
        content = f.read()
    assert "функция unction error_function вызвала исключение: что-то пошло не так" in content