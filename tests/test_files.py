import pandas as pd
from src.utils import file_exists, save_pandas_data

def test_file_exists():
    assert file_exists(path="./data/raw/fcps.xlsx")
    assert not file_exists(path="./data/raw/notExistingData.xlsx")

def test_save_pandas_data():
    data = pd.DataFrame({
        "A": [1, 2],
        "B": [3, 4],
        "C": [5, 6]
    })
    assert not file_exists(path="./data/raw/test_data.xlsx")
    save_pandas_data(input_data=data, filepath="./data/raw/test_data.xlsx")
    assert file_exists(path="./data/raw/test_data.xlsx")