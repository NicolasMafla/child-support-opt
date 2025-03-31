from src.utils import money_to_float


def test_money_to_float1():
    assert money_to_float("1,234.56") == 1234.56


def test_money_to_float2():
    assert money_to_float(1234.56) == 1234.56
