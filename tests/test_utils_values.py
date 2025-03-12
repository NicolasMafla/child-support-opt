from src.utils import money_to_float

def test_money_to_float():
    assert money_to_float("1,234.56") == 1234.56