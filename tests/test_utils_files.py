import pandas as pd
from src.utils import file_exists, save_pandas_data, get_filename, list_files

def test_file_exists():
    assert file_exists(path="./data/test/fcps.xlsx")
    assert not file_exists(path="./data/test/notExistingData.xlsx")

def test_save_pandas_data():
    data = pd.DataFrame({
        "A": [1, 2],
        "B": [3, 4],
        "C": [5, 6]
    })
    assert not file_exists(path="./data/test/test_data.xlsx")
    save_pandas_data(input_data=data, filepath="./data/test/test_data.xlsx")
    assert file_exists(path="./data/test/test_data.xlsx")

def test_get_filename():
    filepath = "./data/test/EC0107.csv"
    filename = get_filename(filepath=filepath)
    assert filename == "EC0107"


def test_list_files():
    path = "./data/test/"
    files = list_files(path=path)
    assert len(files) == 4