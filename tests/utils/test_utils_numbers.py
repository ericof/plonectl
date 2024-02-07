from plonectl.utils import numbers

import pytest


@pytest.mark.parametrize(
    "value,expected",
    [
        [1, "1b"],
        [1_024, "1.00Kb"],
        [4_900, "4.79Kb"],
        [1_000_000, "976.56Kb"],
        [1_048_577, "1.00Mb"],
        [2_000_000, "1.91Mb"],
        [3_000_000_000, "2.79Gb"],
        [1_099_511_627_776, "1.00Tb"],
    ],
)
def test_format_bytes(value: int, expected: str):
    result = numbers.format_bytes(value)
    assert result == expected


@pytest.mark.parametrize(
    "value,expected",
    [[1, "1"], [1_024, "1,024"], [1_000_000, "1,000,000"], [20_000_000, "20,000,000"]],
)
def test_format_int(value: int, expected: str):
    result = numbers.format_int(value)
    assert result == expected
