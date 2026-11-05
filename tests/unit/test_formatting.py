import pytest

from src.helpers.formatting import format_duration


@pytest.mark.parametrize(
    ("milliseconds", "expected"),
    [
        (0, "0:00"),
        (999, "0:00"),
        (1_000, "0:01"),
        (59_999, "0:59"),
        (60_000, "1:00"),
        (3_599_000, "59:59"),
        (3_600_000, "60:00"),
    ],
)
def test_format_duration(milliseconds: int, expected: str) -> None:
    assert format_duration(milliseconds) == expected
