import json
import os
from unittest.mock import mock_open, patch

import pytest

from src.utils import dictionary_with_transaction_data


def test_json_decode_error() -> None:
    mock_file = mock_open(read_data="Invalid JSON")
    with patch("os.path.exists", return_value=True):
        with patch("builtins.open", mock_file):
            with patch(
                "json.load",
                side_effect=json.JSONDecodeError("Error", "doc", 0),
            ):
                result = list(dictionary_with_transaction_data())
                assert result == []


def test_json_not_a_list() -> None:
    # JSON возвращает объект, а не список
    data = {"key": "value"}
    mock_file = mock_open(read_data=json.dumps(data))
    with patch("os.path.exists", return_value=True):
        with patch("builtins.open", mock_file):
            # В случае с json.load вернёт объект
            # если не список, по условию
            result = list(dictionary_with_transaction_data())
            assert result == []
