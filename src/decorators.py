import functools
import traceback
from typing import Any, Callable, Optional

def log(filename: Optional[str] = None) -> Callable[[Callable], Callable]:
    """Декоратор для логирования запуска, результата и ошибок функции.
    Если filename задан, логи пишутся в файл, иначе — в консоль."""

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            msg_start = f"Начало выполнения функции {func.__name__}"
            msg_end = f"Функция {func.__name__} выполнена успешно"
            try:
                _write_log(msg_start, filename)
                output = func(*args, **kwargs)
                msg_result = f"Результат: {output}"
                _write_log(msg_result, filename)
                _write_log(msg_end, filename)
                return output
            except Exception as e:
                msg_error = (
                    f"Ошибка в функции {func.__name__}: "
                    f"{e}\n{traceback.format_exc()}"
                )
                _write_log(msg_error, filename)
                raise

        return wrapper

    return decorator

def _write_log(message: str, filename: Optional[str])-> None:
    """Если filename задан, пишет логи в файл,
    иначе выводит сообщение в консоль."""
    if filename:
        with open(filename, "a", encoding="utf-8") as f:
            f.write(message + "\n")
    else:
        print(message)

@log()  # Логи будут выводиться в консоль
def my_func(x: int, y: int) -> int:
    return x + y

@log("mylog.txt")  # Логи будут записываться в файл my_log.txt
def my_other_func(a: int, b: int) -> int:
    return a * b

# Вызов функций
print()
print(my_func(3, 5))
print(my_other_func(4, 2))